#!/usr/bin/env python3
"""Historical maximum-power tracking for the CALM wiki power measurements.

For every microscope with more than one measurement run, this builds:

* ``power_history.csv`` — one row per run, one column per channel, holding the
  power at the highest voltage of that run;
* ``power_history.svg`` — that same table plotted, date on the x-axis.

Both live in ``assets/power/<WikiBasename>/`` (alongside the per-run folders)
and are regenerated from scratch whenever that microscope gains a measurement,
so they never drift from the underlying CSVs.

"Maximum power" is the power at the highest voltage in the sweep, not the
largest value observed: some channels saturate and then sag, and it is the
top-of-range figure that is meaningful to track. The sweep's top voltage is
recorded in the CSV so a change in measurement range is visible rather than
silently distorting the trend.

The plot is emitted as SVG built by hand — it keeps the script dependency-free
beyond Pillow, stays sharp at any zoom, and costs a few KB.
"""

from __future__ import annotations

import csv
from pathlib import Path

POWER_SUFFIX = "_Power(W)"
HISTORY_CSV = "power_history.csv"
HISTORY_SVG = "power_history.svg"

# Series colours, reused cyclically. Chosen to stay legible on both light and
# dark page backgrounds and to remain distinguishable for common forms of
# colour-vision deficiency.
SERIES_COLORS = [
    "#1f77b4", "#2ca02c", "#ff7f0e", "#d62728",
    "#9467bd", "#8c564b", "#17becf", "#e377c2",
]


def _data_rows(csv_path: Path) -> tuple[list[str] | None, list[list[str]]]:
    """Return (header, data rows) from a measurement CSV.

    Tolerates the ``#`` comment preamble, blank lines, and files where the
    header line is repeated part-way through (seen in at least one early
    measurement).
    """
    header: list[str] | None = None
    rows: list[list[str]] = []
    text = csv_path.read_text(encoding="utf-8", errors="replace")
    body = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    for row in csv.reader(body):
        if not row:
            continue
        if row[0].strip().lower() == "voltage":
            header = row  # (re-)establish the header; later copies are identical
            continue
        if header is not None:
            rows.append(row)
    return header, rows


def channels_of(header: list[str]) -> list[tuple[str, int]]:
    """Channel names and their column indices, in file order."""
    return [
        (name[: -len(POWER_SUFFIX)], i)
        for i, name in enumerate(header)
        if name.endswith(POWER_SUFFIX)
    ]


def max_voltage_powers(csv_path: Path) -> tuple[float | None, dict[str, float]]:
    """Power (in mW) per channel at the highest voltage of this run.

    Returns ``(voltage, {channel: mW})``. The voltage is None for a run with no
    parseable voltage column — a single-point measurement, which still yields
    usable per-channel powers from its one row.
    """
    header, rows = _data_rows(csv_path)
    if header is None or not rows:
        return None, {}

    best_v: float | None = None
    best_row: list[str] | None = None
    for row in rows:
        try:
            v = float(row[0])
        except (ValueError, IndexError):
            continue
        if v != v:  # NaN: a single-point run with no voltage sweep
            continue
        if best_v is None or v > best_v:
            best_v, best_row = v, row
    if best_row is None:
        # No numeric voltage anywhere (e.g. a "NaN" single-point run): fall back
        # to the last data row so the channel powers are still captured.
        best_row = rows[-1]

    powers: dict[str, float] = {}
    for name, idx in channels_of(header):
        try:
            powers[name] = float(best_row[idx]) * 1000.0  # W -> mW
        except (ValueError, IndexError):
            continue
    return best_v, powers


def collect_history(runs) -> tuple[list[str], list[dict]]:
    """Build the history table from measurement runs.

    ``runs`` is any iterable of objects exposing ``csv`` and ``display_date``
    (i.e. ``Measurement``). Returns ``(channel_names, points)`` ordered oldest
    first, where each point is ``{date, voltage, powers}``.

    Channels are unioned across runs so that a channel added or removed partway
    through the history still gets a column; a run missing one leaves a gap
    rather than breaking the series.
    """
    points: list[dict] = []
    channels: list[str] = []
    for run in sorted(runs, key=lambda r: r.key):
        voltage, powers = max_voltage_powers(run.csv)
        if not powers:
            continue
        for name in powers:
            if name not in channels:
                channels.append(name)
        points.append({
            "date": run.display_date,
            "voltage": voltage,
            "powers": powers,
        })
    return channels, points


def write_history_csv(dest: Path, channels: list[str], points: list[dict]) -> None:
    """Write the historical maximum-power table."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="") as fh:
        # The preamble is written directly rather than through csv.writer, which
        # would quote any comment line containing a comma.
        fh.write("# Historical maximum power per channel, in mW.\r\n")
        fh.write("# Power is taken at the highest voltage of each sweep;\r\n")
        fh.write("# that voltage is given in the Voltage column.\r\n")
        fh.write("# Generated by script/power_measurements - do not edit.\r\n")
        w = csv.writer(fh)
        w.writerow(["Date", "Voltage(V)"] + [f"{c}_Power(mW)" for c in channels])
        for p in points:
            volt = "" if p["voltage"] is None else f"{p['voltage']:g}"
            w.writerow(
                [p["date"], volt]
                + [
                    "" if c not in p["powers"] else f"{p['powers'][c]:.6g}"
                    for c in channels
                ]
            )


# ---------------------------------------------------------------------------
# SVG plot
# ---------------------------------------------------------------------------

def _nice_ticks(lo: float, hi: float, target: int = 6) -> list[float]:
    """Human-friendly axis ticks covering [lo, hi]."""
    if hi <= lo:
        hi = lo + 1.0
    raw = (hi - lo) / target
    mag = 10 ** _floor_log10(raw)
    for mult in (1, 2, 2.5, 5, 10):
        step = mag * mult
        if step >= raw:
            break
    start = step * int(lo / step)
    if start > lo:
        start -= step
    ticks = []
    v = start
    while v <= hi + step * 0.5:
        if v >= lo - step * 0.5:
            ticks.append(round(v, 10))
        v += step
    return ticks


def _floor_log10(x: float) -> int:
    import math
    return int(math.floor(math.log10(x))) if x > 0 else 0


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def render_history_svg(title: str, channels: list[str], points: list[dict]) -> str:
    """Render the historical maximum-power plot as a standalone SVG string.

    Dates sit on the x-axis at equal spacing (measurements are irregular and
    sparse; even spacing keeps labels readable and comparisons honest). Colours
    are set via CSS custom properties so the plot follows the page's light or
    dark theme.
    """
    W = 820
    # Generous left/bottom margins: the x labels are rotated date-times, which
    # would otherwise run off the left edge and under the legend.
    ml, mr, mt = 92, 30, 52
    # Grow the canvas so the legend always clears the rotated x labels, however
    # many channels this microscope has.
    _per_row = max(1, (W - ml - mr) // 190)
    _legend_rows = (len(channels) + _per_row - 1) // _per_row
    mb = 96 + _legend_rows * 17
    H = 400 + mb
    pw, ph = W - ml - mr, H - mt - mb

    vals = [p["powers"][c] for p in points for c in channels if c in p["powers"]]
    lo, hi = (0.0, 1.0) if not vals else (min(vals), max(vals))
    lo = min(lo, 0.0)  # always anchor at zero: these are absolute powers
    ticks = _nice_ticks(lo, hi)
    ymin, ymax = min(ticks[0], lo), max(ticks[-1], hi)

    def x_of(i: int) -> float:
        if len(points) == 1:
            return ml + pw / 2
        return ml + pw * i / (len(points) - 1)

    def y_of(v: float) -> float:
        return mt + ph * (1 - (v - ymin) / (ymax - ymin or 1))

    out: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="{_esc(title)}" '
        'style="max-width:100%;height:auto;font-family:system-ui,-apple-system,'
        'Segoe UI,Roboto,sans-serif">',
        # Theme-aware palette. The page's own colours win where available.
        "<style>"
        ".hp-bg{fill:#fff}.hp-fg{fill:#222}.hp-ax{stroke:#666}.hp-gr{stroke:#ddd}"
        "@media (prefers-color-scheme:dark){"
        ".hp-bg{fill:#0d1117}.hp-fg{fill:#e6edf3}"
        ".hp-ax{stroke:#8b949e}.hp-gr{stroke:#30363d}}"
        "</style>",
        f'<rect class="hp-bg" x="0" y="0" width="{W}" height="{H}"/>',
        f'<text class="hp-fg" x="{W/2:.0f}" y="26" text-anchor="middle" '
        f'font-size="16" font-weight="600">{_esc(title)}</text>',
    ]

    # Horizontal gridlines + y tick labels.
    for t in ticks:
        y = y_of(t)
        out.append(f'<line class="hp-gr" x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" '
                   f'y2="{y:.1f}" stroke-dasharray="3 3"/>')
        out.append(f'<text class="hp-fg" x="{ml-9}" y="{y+4:.1f}" '
                   f'text-anchor="end" font-size="11">{t:g}</text>')

    # Axes.
    out.append(f'<line class="hp-ax" x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}"/>')
    out.append(f'<line class="hp-ax" x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" '
               f'y2="{mt+ph}"/>')
    out.append(f'<text class="hp-fg" x="18" y="{mt+ph/2:.0f}" font-size="12" '
               f'text-anchor="middle" transform="rotate(-90 18 {mt+ph/2:.0f})">'
               "Power (mW)</text>")

    # X tick labels: date above time, angled to avoid collisions.
    for i, p in enumerate(points):
        x = x_of(i)
        day, _, hm = p["date"].partition(" ")
        out.append(f'<line class="hp-gr" x1="{x:.1f}" y1="{mt}" x2="{x:.1f}" '
                   f'y2="{mt+ph}" stroke-dasharray="3 3"/>')
        out.append(
            f'<text class="hp-fg" x="{x:.1f}" y="{mt+ph+16}" font-size="11" '
            f'text-anchor="end" transform="rotate(-40 {x:.1f} {mt+ph+16})">'
            f'{_esc(day)} {_esc(hm)}</text>'
        )

    # One polyline + markers per channel, skipping gaps.
    for ci, chan in enumerate(channels):
        color = SERIES_COLORS[ci % len(SERIES_COLORS)]
        pts = [(x_of(i), y_of(p["powers"][chan]))
               for i, p in enumerate(points) if chan in p["powers"]]
        if not pts:
            continue
        if len(pts) > 1:
            d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            out.append(f'<polyline fill="none" stroke="{color}" '
                       f'stroke-width="2" points="{d}"/>')
        for x, y in pts:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" '
                       f'fill="{color}"><title>{_esc(chan)}: '
                       f'{_fmt_at(points, chan, x, x_of)}</title></circle>')

    # Legend, wrapped across rows so many channels still fit. Anchored to the
    # bottom of the canvas, below the rotated x labels.
    per_row = _per_row
    legend_top = H - 8 - (_legend_rows - 1) * 17
    for ci, chan in enumerate(channels):
        color = SERIES_COLORS[ci % len(SERIES_COLORS)]
        row, col = divmod(ci, per_row)
        lx = ml + col * (pw / per_row)
        ly = legend_top + row * 17
        out.append(f'<line x1="{lx:.0f}" y1="{ly-4:.0f}" x2="{lx+16:.0f}" '
                   f'y2="{ly-4:.0f}" stroke="{color}" stroke-width="2"/>')
        out.append(f'<circle cx="{lx+8:.0f}" cy="{ly-4:.0f}" r="3.5" '
                   f'fill="{color}"/>')
        out.append(f'<text class="hp-fg" x="{lx+22:.0f}" y="{ly:.0f}" '
                   f'font-size="11">{_esc(chan)}</text>')

    out.append("</svg>")
    return "\n".join(out)


def _fmt_at(points, chan, x, x_of) -> str:
    """Tooltip text for the marker nearest x (used for hover detail)."""
    for i, p in enumerate(points):
        if abs(x_of(i) - x) < 0.5 and chan in p["powers"]:
            return f"{p['powers'][chan]:.4g} mW on {p['date']}"
    return ""


def write_history(power_dir: Path, wiki_basename: str, runs) -> bool:
    """Write power_history.{csv,svg} for a microscope.

    Returns True if the files were written, False if this microscope does not
    have enough data (fewer than two runs with usable readings) — in which case
    any previously written history files are removed, so a page never links to
    a stale artefact.
    """
    channels, points = collect_history(runs)
    csv_path = power_dir / HISTORY_CSV
    svg_path = power_dir / HISTORY_SVG

    if len(points) < 2 or not channels:
        for stale in (csv_path, svg_path):
            if stale.exists():
                stale.unlink()
        return False

    write_history_csv(csv_path, channels, points)
    voltages = {p["voltage"] for p in points
                if p["voltage"] is not None and p["voltage"] == p["voltage"]}
    if len(voltages) == 1:
        title = (f"Maximum power over time — {wiki_basename} "
                 f"(at {next(iter(voltages)):g} V)")
    else:
        title = f"Maximum power over time — {wiki_basename}"
    svg_path.write_text(render_history_svg(title, channels, points),
                        encoding="utf-8")
    return True
