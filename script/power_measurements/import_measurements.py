#!/usr/bin/env python3
"""Survey a directory of microscope power measurements, move new ones into the
CALM wiki, inject a "Power Measurements" section into the matching wiki
microscope page, and stage a git commit in the wiki repo.

Filename convention (produced by ThorlabsPowerMeasurement*.bsh):

    powerMeasurement_<Microscope>_<YYMMDD>_<HHMM>[_<channel>].{csv,png,jpg}

Each measurement run is anchored by its CSV; the sibling plots share the
``powerMeasurement_<Microscope>_<YYMMDD>_<HHMM>`` prefix. One of them ends in
``_combined`` and is used as the headline plot.

Plots are stored in the wiki as palettised (256-colour) PNGs, and both PNG and
JPEG are accepted as input while the ``.bsh`` writers are migrated from one to
the other:

* an already-palettised PNG is moved through untouched;
* a JPEG, or a 24-bit PNG, is converted (see ``import_image``).

JPEG is a poor fit for these plots — line art on a flat white background — as
its lossy compression both softens the text and smears thousands of noise
colours into what should be a handful of solid ones. Palettising is the step
that matters for size: a plain 24-bit PNG is *larger* than the source JPEG,
because it faithfully stores that JPEG noise, and even for a clean plot it
costs three bytes per pixel regardless of how few colours are in use.

The measurement microscope name is translated to a wiki page basename via a JSON
map (``microscope_map.json`` next to this script). Data is stored in the wiki under
``assets/power/<WikiBasename>/<YYMMDD_HHMM>/`` and the page gets a block bounded by
``POWER:START``/``POWER:END`` markers appended at its end (re-runs replace only
what's between the markers; hand-written content and front matter are untouched).

Pillow is the only third-party dependency (``pip install pillow``), used for the
JPEG-to-PNG conversion. The script is idempotent: a run already present under
``assets/power/`` is skipped, and each page's power block is always regenerated
from the full contents of that microscope's ``assets/power`` folder.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - surfaced to the user at startup
    Image = None

# ---------------------------------------------------------------------------
# Image conversion
# ---------------------------------------------------------------------------

# The plots are line art: axes, gridlines, a few coloured traces and text. A
# 256-colour palette covers that with room to spare, so quantising is visually
# lossless here while roughly halving the file size relative to the source JPEG.
PNG_COLORS = 256

# Plot suffixes accepted from the measurement directory.
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg")


def needs_palettising(path: Path) -> bool:
    """True if ``path`` is a PNG that is already palettised (mode "P").

    A 24-bit PNG stores three bytes per pixel no matter how few colours it
    actually uses, so palettising one of these plots is still a ~2.7x win even
    when it is already clean and lossless. Quantising an image that has at most
    PNG_COLORS distinct colours is exact, so this never costs quality.
    """
    with Image.open(path) as im:
        return im.mode != "P"


def convert_to_png(src: Path, dest_dir: Path) -> Path:
    """Write ``src`` into ``dest_dir`` as a palettised PNG and return the path.

    Dithering is disabled deliberately: on flat backgrounds it would scatter
    isolated pixels that both look wrong and defeat PNG's run-length filtering.
    """
    dest = dest_dir / (src.stem + ".png")
    with Image.open(src) as im:
        rgb = im.convert("RGB")
        rgb.quantize(colors=PNG_COLORS, method=Image.MEDIANCUT,
                     dither=Image.NONE).save(dest, "PNG", optimize=True)
    return dest


def import_image(src: Path, dest_dir: Path) -> tuple[Path, str]:
    """Place one plot into ``dest_dir`` as a PNG. Returns (path, what-happened).

    A PNG that is already palettised is moved through untouched; anything else
    (a JPEG, or a 24-bit PNG from a not-yet-updated .bsh) is converted.
    """
    if src.suffix.lower() == ".png" and not needs_palettising(src):
        dest = dest_dir / src.name
        shutil.move(str(src), str(dest))
        return dest, "moved"
    dest = convert_to_png(src, dest_dir)
    src.unlink()
    return dest, "converted"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

# powerMeasurement_<Microscope>_<YYMMDD>_<HHMM>  (the run prefix)
PREFIX_RE = re.compile(
    r"^powerMeasurement_(?P<mic>.+?)_(?P<date>\d{6})_(?P<time>\d{4})",
    re.IGNORECASE,
)
CSV_RE = re.compile(
    r"^powerMeasurement_(?P<mic>.+?)_(?P<date>\d{6})_(?P<time>\d{4})\.csv$",
    re.IGNORECASE,
)


@dataclass
class Measurement:
    """One measurement run and the files that belong to it."""

    microscope: str          # measurement-side microscope name, e.g. "CVRISD2"
    date: str                # YYMMDD
    time: str                # HHMM
    csv: Path                # the CSV file
    images: list[Path] = field(default_factory=list)  # sibling plots (JPG/PNG in, PNG out)
    # Duplicate source plots losing to a preferred one (a JPEG alongside the
    # same plot as PNG). Deleted on import so they are not seen again.
    superseded: list[Path] = field(default_factory=list)

    @property
    def key(self) -> str:
        """Timestamp key used for the data folder name, e.g. '260721_1216'."""
        return f"{self.date}_{self.time}"

    @property
    def prefix(self) -> str:
        return f"powerMeasurement_{self.microscope}_{self.date}_{self.time}"

    @property
    def display_date(self) -> str:
        """Human date derived from the YYMMDD_HHMM key: 'YYYY-MM-DD HH:MM'."""
        yy, mm, dd = self.date[0:2], self.date[2:4], self.date[4:6]
        hh, mi = self.time[0:2], self.time[2:4]
        return f"20{yy}-{mm}-{dd} {hh}:{mi}"

    def combined_image_name(self) -> str | None:
        # Accept .jpg as well as .png so a not-yet-converted source run still
        # resolves; imported runs are always PNG.
        for img in self.images:
            if Path(img.name.lower()).stem.endswith("_combined"):
                return img.name
        return None


def read_csv_header(csv_path: Path) -> dict[str, str]:
    """Return the ``# Key: Value`` comment header of a measurement CSV."""
    header: dict[str, str] = {}
    try:
        with csv_path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not line.startswith("#"):
                    break
                body = line[1:].strip()
                if ":" in body:
                    key, _, value = body.partition(":")
                    header[key.strip()] = value.strip()
    except OSError:
        pass
    return header


def parse_measurement_filename(name: str) -> dict[str, str] | None:
    """Parse a run prefix out of a filename, or None if it doesn't match."""
    m = PREFIX_RE.match(name)
    if not m:
        return None
    return {"microscope": m.group("mic"), "date": m.group("date"), "time": m.group("time")}


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_source_measurements(source: Path) -> list[Measurement]:
    """Find measurement runs in a source directory, anchored by each CSV."""
    measurements: list[Measurement] = []
    for csv_path in sorted(source.glob("powerMeasurement_*.csv")):
        m = CSV_RE.match(csv_path.name)
        if not m:
            continue
        # Prefer the microscope name from the CSV header when present.
        header = read_csv_header(csv_path)
        mic = header.get("Microscope") or m.group("mic")
        meas = Measurement(
            microscope=mic,
            date=m.group("date"),
            time=m.group("time"),
            csv=csv_path,
        )
        # Collect sibling plots that share the same run prefix (case-insensitive).
        # Both PNG and JPEG are accepted, since the .bsh writers are being
        # migrated from one to the other. If a plot happens to be present as
        # both, keep the PNG: it is the newer, non-lossy one.
        prefix = f"powerMeasurement_{m.group('mic')}_{m.group('date')}_{m.group('time')}".lower()
        by_stem: dict[str, Path] = {}
        for img in source.iterdir():
            if img.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            if not img.name.lower().startswith(prefix):
                continue
            stem = img.stem.lower()
            if stem not in by_stem:
                by_stem[stem] = img
            elif img.suffix.lower() == ".png":
                meas.superseded.append(by_stem[stem])
                by_stem[stem] = img
            else:
                meas.superseded.append(img)
        meas.images.extend(by_stem.values())
        meas.images.sort(key=lambda p: p.name.lower())
        measurements.append(meas)
    return measurements


def discover_wiki_runs(wiki: Path, wiki_basename: str) -> list[Measurement]:
    """Scan assets/power/<wiki_basename>/ and return its runs, newest first.

    Each ``assets/power/<wiki_basename>/<YYMMDD_HHMM>/`` folder is one run.
    """
    runs: list[Measurement] = []
    power_dir = wiki / "assets" / "power" / wiki_basename
    if not power_dir.is_dir():
        return runs
    for run_dir in sorted(p for p in power_dir.iterdir() if p.is_dir()):
        csvs = list(run_dir.glob("*.csv"))
        if not csvs:
            continue
        csv_path = csvs[0]
        info = parse_measurement_filename(csv_path.name)
        if info:
            date, time = info["date"], info["time"]
        else:
            dm = re.match(r"^(\d{6})_(\d{4})$", run_dir.name)
            if not dm:
                continue
            date, time = dm.group(1), dm.group(2)
        runs.append(
            Measurement(
                microscope=wiki_basename,
                date=date,
                time=time,
                csv=csv_path,
                images=sorted(run_dir.glob("*.png"), key=lambda p: p.name.lower()),
            )
        )
    runs.sort(key=lambda mm: mm.key, reverse=True)  # newest first
    return runs


# ---------------------------------------------------------------------------
# Moving
# ---------------------------------------------------------------------------

def import_measurement(meas: Measurement, wiki: Path, wiki_basename: str,
                       dry_run: bool) -> Path | None:
    """Import a run into assets/power/<wiki_basename>/<key>/. The CSV is moved
    as-is; each plot is stored as a PNG (see ``import_image``). Return the
    destination, or None if it already existed (skipped)."""
    dest = wiki / "assets" / "power" / wiki_basename / meas.key
    if dest.exists():
        return None  # already imported
    if dry_run:
        return dest
    dest.mkdir(parents=True, exist_ok=True)
    shutil.move(str(meas.csv), str(dest / meas.csv.name))
    for img in meas.images:
        import_image(img, dest)
    for img in meas.superseded:
        img.unlink()  # a duplicate of a plot already imported in better form
    return dest


def backfill_pngs(wiki: Path, dry_run: bool) -> int:
    """Normalise plots already under assets/power/ to palettised PNG.

    Handles both leftovers from before the PNG switch (JPEGs) and 24-bit PNGs
    from a .bsh that writes PNG but does not palettise. Runs on every
    invocation so the tree converges; it is a no-op once everything is a
    palettised PNG. Returns the number of files dealt with."""
    power_root = wiki / "assets" / "power"
    if not power_root.is_dir():
        return 0
    stale: list[Path] = sorted(
        p for p in power_root.rglob("*")
        if p.suffix.lower() in (".jpg", ".jpeg")
    )
    stale += sorted(
        p for p in power_root.rglob("*.png") if needs_palettising(p)
    )
    for img in stale:
        if dry_run:
            print(f"  would convert {img.relative_to(wiki)}")
            continue
        png = img.with_suffix(".png")
        # A JPEG whose PNG already exists is just dropped; a 24-bit PNG is
        # replaced in place (convert_to_png writes to the same name).
        if img.suffix.lower() == ".png" or not png.exists():
            convert_to_png(img, img.parent)
        if img != png:
            img.unlink()
        print(f"  converted {img.relative_to(wiki)} -> {png.name}")
    return len(stale)


# ---------------------------------------------------------------------------
# Power section generation
# ---------------------------------------------------------------------------

POWER_START = "<!-- POWER:START (generated by microscope_power importer — do not edit) -->"
POWER_END = "<!-- POWER:END -->"


def asset_url(rel: str) -> str:
    """A Liquid expression resolving an asset path under the wiki baseurl."""
    return "{{ '/" + rel + "' | relative_url }}"


def render_power_block(wiki_basename: str, runs: list[Measurement]) -> str:
    """Build the marker-delimited Power Measurements block for a wiki page."""
    latest = runs[0]
    latest_combined = latest.combined_image_name()
    img_id = "combined-plot"
    csv_id = "csv-link"

    def run_dir(mm: Measurement) -> str:
        return f"assets/power/{wiki_basename}/{mm.key}"

    lines = [
        POWER_START,
        "## Power Measurements",
        "",
        f"Most recent measurement: **{latest.display_date}**",
        "",
    ]

    # Headline combined plot.
    if latest_combined:
        img_src = asset_url(f"{run_dir(latest)}/{latest_combined}")
        lines += [
            f'<img id="{img_id}" src="{img_src}" '
            f'alt="Combined power plot — {latest.display_date}" '
            'style="max-width:100%;height:auto;" />',
            "",
        ]
    else:
        lines += ["_No combined plot available for the latest measurement._", ""]

    # CSV download link.
    csv_src = asset_url(f"{run_dir(latest)}/{latest.csv.name}")
    lines += [
        f'<p><a id="{csv_id}" href="{csv_src}" download>Download CSV data</a></p>',
        "",
    ]

    # Date dropdown.
    lines += [
        "**Browse measurements:**",
        "",
        f'<select class="measurement-picker" '
        f'data-img-target="{img_id}" data-csv-target="{csv_id}">',
    ]
    for mm in runs:
        combined = mm.combined_image_name()
        img_attr = asset_url(f"{run_dir(mm)}/{combined}") if combined else ""
        csv_attr = asset_url(f"{run_dir(mm)}/{mm.csv.name}")
        lines.append(
            f'  <option data-img="{img_attr}" data-csv="{csv_attr}">'
            f"{mm.display_date}</option>"
        )
    lines.append("</select>")
    lines.append("")

    # Wire up the dropdown behaviour.
    js_src = asset_url("assets/js/measurement-switch.js")
    lines += [f'<script src="{js_src}"></script>', POWER_END]
    return "\n".join(lines)


def upsert_power_block(page: Path, block: str) -> None:
    """Replace the POWER block in a page, or append it if not present."""
    text = page.read_text(encoding="utf-8")
    if POWER_START in text and POWER_END in text:
        start = text.index(POWER_START)
        end = text.index(POWER_END) + len(POWER_END)
        new_text = text[:start] + block + text[end:]
    else:
        sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        new_text = text + sep + "\n" + block + "\n"
    page.write_text(new_text, encoding="utf-8")


def ensure_front_matter(page: Path) -> bool:
    """Ensure a wiki page has YAML front matter so Jekyll renders it (Liquid
    tags, theme layout). If it already has front matter — with or without a
    leading UTF-8 BOM — do nothing. Otherwise prepend a minimal
    ``layout: default`` block, taking the title from the first ``# `` heading.
    Returns True if the page was modified."""
    text = page.read_text(encoding="utf-8")
    stripped = text.lstrip("﻿")  # tolerate a BOM
    if stripped.startswith("---"):
        return False
    title = page.stem
    m = re.search(r"^#\s+(.+?)\s*$", stripped, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    # Quote the title so ``#`` / ``:`` in headings stay valid YAML.
    front = f'---\nlayout: default\ntitle: "{title}"\n---\n\n'
    page.write_text(front + stripped, encoding="utf-8")
    print(f"  added front matter to {page.name} (title: {title})")
    return True


# ---------------------------------------------------------------------------
# Shared JS asset
# ---------------------------------------------------------------------------

# The dropdown behaviour, shipped into the wiki at assets/js/measurement-switch.js.
SWITCH_JS = """\
// Swap the displayed combined plot and the CSV download link when the user
// picks a different measurement date. Each <option> carries data-img / data-csv
// attributes (already prefixed with the site baseurl by the page generator).
// Generated by script/power_measurements/import_measurements.py — do not edit.
(function () {
  function wire(select) {
    var imgId = select.getAttribute("data-img-target");
    var csvId = select.getAttribute("data-csv-target");
    var img = document.getElementById(imgId);
    var csv = document.getElementById(csvId);
    select.addEventListener("change", function () {
      var opt = select.options[select.selectedIndex];
      if (img && opt.getAttribute("data-img")) {
        img.src = opt.getAttribute("data-img");
        img.alt = "Combined power plot — " + opt.textContent;
      }
      if (csv && opt.getAttribute("data-csv")) {
        csv.href = opt.getAttribute("data-csv");
      }
    });
  }
  document.addEventListener("DOMContentLoaded", function () {
    var selects = document.querySelectorAll("select.measurement-picker");
    for (var i = 0; i < selects.length; i++) {
      wire(selects[i]);
    }
  });
})();
"""


def ensure_switch_js(wiki: Path) -> None:
    """Write measurement-switch.js into the wiki's assets/js/ if missing or stale."""
    dest = wiki / "assets" / "js" / "measurement-switch.js"
    if dest.exists() and dest.read_text(encoding="utf-8") == SWITCH_JS:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(SWITCH_JS, encoding="utf-8")
    print(f"  wrote measurement-switch.js -> {dest.relative_to(wiki)}")


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def is_git_repo(repo: Path) -> bool:
    return (repo / ".git").exists()


def git_commit(repo: Path, imported: list[Measurement],
               name_for: dict[str, str]) -> None:
    if not is_git_repo(repo):
        print("  (wiki is not a git repository; skipping commit)")
        return
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    status = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    )
    if not status.stdout.strip():
        print("  (nothing to commit)")
        return
    if imported:
        summary = ", ".join(
            f"{name_for.get(m.microscope, m.microscope)} {m.display_date}"
            for m in imported
        )
        message = f"Add {len(imported)} power measurement(s): {summary}"
    else:
        message = "Regenerate power measurement sections"
    subprocess.run(["git", "-C", str(repo), "commit", "-m", message], check=True)
    print(f"  committed to wiki: {message}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_map(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: list[str] | None = None) -> int:
    script_dir = Path(__file__).resolve().parent
    # The script lives at <wiki>/script/power_measurements/; the wiki root is two
    # levels up. That is the default target so the tool "just works" in place.
    default_wiki = script_dir.parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path,
                        help="directory of incoming power measurements")
    parser.add_argument("--wiki", default=default_wiki, type=Path,
                        help="path to the UCSF-CALM-wiki repository "
                             "(default: the repo this script lives in)")
    parser.add_argument("--map", default=script_dir / "microscope_map.json",
                        type=Path,
                        help="JSON map: measurement name -> wiki page basename")
    parser.add_argument("--no-commit", action="store_true",
                        help="do everything except git add/commit in the wiki")
    parser.add_argument("--dry-run", action="store_true",
                        help="report the plan; move nothing, write nothing")
    args = parser.parse_args(argv)

    source = args.source
    wiki = args.wiki.expanduser().resolve()

    if not source.is_dir():
        print(f"error: source directory not found: {source}", file=sys.stderr)
        return 2
    if not wiki.is_dir():
        print(f"error: wiki directory not found: {wiki}", file=sys.stderr)
        return 2
    if not args.map.is_file():
        print(f"error: map file not found: {args.map}", file=sys.stderr)
        return 2
    if Image is None:
        print("error: Pillow is required for JPEG->PNG conversion "
              "(pip install pillow)", file=sys.stderr)
        return 2

    name_map = load_map(args.map)

    print(f"Surveying {source} ...")
    found = discover_source_measurements(source)
    print(f"  found {len(found)} measurement run(s) in source")

    imported: list[Measurement] = []
    affected_pages: dict[str, str] = {}  # wiki_basename -> source microscope name
    for meas in found:
        wiki_basename = name_map.get(meas.microscope)
        if wiki_basename is None:
            print(f"  ! skip (no map entry): {meas.microscope} "
                  f"— add it to {args.map.name}", file=sys.stderr)
            continue
        page = wiki / "pages" / "microscopes" / f"{wiki_basename}.md"
        if not page.is_file():
            print(f"  ! skip ({meas.microscope} -> {wiki_basename}): "
                  f"page not found at {page}", file=sys.stderr)
            continue

        dest = import_measurement(meas, wiki, wiki_basename, args.dry_run)
        if dest is None:
            print(f"  skip (already imported): {meas.prefix}")
        else:
            verb = "would move" if args.dry_run else "moved"
            print(f"  {verb} {meas.prefix} -> "
                  f"assets/power/{wiki_basename}/{meas.key} "
                  f"({1 + len(meas.images)} file(s))")
            imported.append(meas)
        affected_pages[wiki_basename] = meas.microscope

    if args.dry_run:
        print("\nChecking assets/power for plots needing conversion ...")
        if not backfill_pngs(wiki, dry_run=True):
            print("  none")
        if affected_pages:
            print("\nPages that would get a Power Measurements block:")
            for basename in sorted(affected_pages):
                print(f"  pages/microscopes/{basename}.md")
        print("\nDry run: no files moved, no pages written, no commit.")
        return 0

    # Convert any JPEGs imported before the PNG switch. Must happen before the
    # pages are regenerated below, so they reference the .png names.
    converted = backfill_pngs(wiki, dry_run=False)
    if converted:
        print(f"\nNormalised {converted} existing plot(s) to palettised PNG")

    # Regenerate the power block on every mapped page that has data under
    # assets/power/ (not just ones touched by this run). This keeps all pages
    # up to date and self-healing — e.g. after a template or front-matter fix —
    # even when the source directory is empty.
    ensure_switch_js(wiki)
    pages_to_update = set(affected_pages)
    power_root = wiki / "assets" / "power"
    for basename in name_map.values():
        if (power_root / basename).is_dir():
            pages_to_update.add(basename)

    print(f"\nUpdating {len(pages_to_update)} wiki page(s) ...")
    for wiki_basename in sorted(pages_to_update):
        page = wiki / "pages" / "microscopes" / f"{wiki_basename}.md"
        if not page.is_file():
            print(f"  ! skip {wiki_basename}: page not found at {page}",
                  file=sys.stderr)
            continue
        runs = discover_wiki_runs(wiki, wiki_basename)
        if not runs:
            continue
        block = render_power_block(wiki_basename, runs)
        ensure_front_matter(page)
        upsert_power_block(page, block)
        print(f"  updated pages/microscopes/{wiki_basename}.md "
              f"({len(runs)} measurement(s))")

    if args.no_commit:
        print("\n--no-commit: wiki changes staged nothing; review with "
              "`git -C <wiki> status`.")
    else:
        print("\nStaging commit in wiki ...")
        git_commit(wiki, imported, name_map)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
