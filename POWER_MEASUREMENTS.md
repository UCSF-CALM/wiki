# Power Measurements

Light-source power measurements are published on each microscope's wiki page as a
**Power Measurements** section (latest combined plot, a CSV download link, and a
date dropdown to browse every past run). The section is generated and kept up to
date by `script/power_measurements/import_measurements.py`.

## How it works

Each microscope runs a Beanshell script (`ThorlabsPowerMeasurement*.bsh`) that
writes, per measurement run, into a shared directory (e.g. `Z:\PowerMeasurements`):

- one CSV: `powerMeasurement_<Microscope>_<YYMMDD>_<HHMM>.csv`
- one combined plot: `..._combined.{png,jpg}`
- one plot per channel: `..._<channel>.{png,jpg}`

Both PNG and JPEG are accepted, so the `.bsh` writers can be switched from one
to the other microscope by microscope, in any order, with no coordination
needed. Plots are always stored in the wiki as palettised PNGs — see
[Why PNG](#why-png).

The importer surveys that directory and, for each new run:

1. Translates the measurement microscope name to a wiki page basename using
   `script/power_measurements/microscope_map.json`.
2. **Moves** the CSV into the wiki at
   `assets/power/<WikiBasename>/<YYMMDD_HHMM>/`, normalising each plot to a
   palettised PNG on the way in: an already-palettised PNG is moved through
   untouched, while a JPEG or a 24-bit PNG is converted. If a plot is present
   as both PNG and JPEG, the PNG wins and the JPEG is discarded.
3. Rewrites the `## Power Measurements` block (bounded by `POWER:START` /
   `POWER:END` markers) at the bottom of
   `pages/microscopes/<WikiBasename>.md`. Everything above the markers —
   front matter and all hand-written content — is left untouched.
4. Stages a git commit in this repo. **It does not push.**

Needs Python 3.9+ and Pillow (`pip install pillow`). The tool is idempotent:
a run already under `assets/power/` is skipped, and every mapped page's block is
regenerated from what's on disk, so re-running is always safe.

## Why PNG

JPEG is the wrong format for these plots — they are line art on a flat white
background, and its lossy compression both softens the text and smears thousands
of noise colours into what should be a handful of solid ones. Where a `.bsh`
still writes JPEG, the importer converts it.

**Palettising is the step that actually saves space**, and it is worth doing
even once every `.bsh` writes PNG. Measured over the 22 plots present when this
was introduced:

| Format | Total size | vs JPEG |
| --- | --- | --- |
| JPEG (source) | 2775 KB | — |
| PNG, 24-bit | 3034 KB | 1.09x |
| **PNG, 256-colour** | **1267 KB** | **0.46x** |

A plain 24-bit PNG is *larger* than the source JPEG, because it faithfully
stores the JPEG's noise. And a 24-bit PNG costs three bytes per pixel however
few colours are in use, so even a clean plot straight from a fixed `.bsh` is
~2.7x larger than its palettised form (measured on a 249-colour plot: 89 KB vs
33 KB). Hence the rule: a PNG that is already palettised is passed through
byte-for-byte, anything else is quantised.

256 colours is far more than these plots use, so the result is visually
indistinguishable — mean per-pixel error 0.33/255, and the only pixels that
shift are anti-aliased glyph edges, which get *cleaner* as JPEG ringing is
discarded. Quantising an image that already has ≤256 colours is exact, so the
pass costs nothing in quality. Dithering is disabled: on flat backgrounds it
would scatter isolated pixels that look wrong and defeat PNG's run-length
filtering.

Anything under `assets/power/` that is not already a palettised PNG — a
leftover JPEG, or a 24-bit PNG — is normalised on the next run, so the tree
converges without a separate migration step.

## Running it

From the root of this repository:

```sh
# 1. Preview — reports what would happen, moves and writes nothing:
python script/power_measurements/import_measurements.py \
    --source Z:\PowerMeasurements --dry-run

# 2. Do it — move new data in, update pages, stage a commit:
python script/power_measurements/import_measurements.py \
    --source Z:\PowerMeasurements

# 3. Review and publish:
git log -1 --stat
git push          # the site's Pages workflow then deploys
```

`--wiki` and `--map` default to this repository and the map beside the script, so
normally only `--source` is needed.

Options:

| Flag | Meaning |
|---|---|
| `--source PATH` | directory of incoming measurements (**required**) |
| `--wiki PATH`   | wiki repo root (default: the repo this script lives in) |
| `--map PATH`    | translation table (default: `microscope_map.json` beside the script) |
| `--no-commit`   | do everything except `git add` / `git commit` |
| `--dry-run`     | report the plan; move nothing, write nothing |

## Adding a microscope

Add one line to `script/power_measurements/microscope_map.json`, mapping the
measurement-side name (as it appears in the filename / the CSV `# Microscope:`
header) to the wiki page basename (the `.md` filename without the extension):

```json
{
  "Timelapse2": "QLIPP-Timelapse-with-Nanoindentor",
  "CVRISD2": "CVRI-NikonSpinningDiskConfocal2"
}
```

A measurement whose name is not in the map is reported and skipped — it is never
guessed. On the next run after adding the entry, that microscope's page picks up
its measurements automatically.

## Notes

- The importer ensures each target page has YAML front matter (adding a minimal
  `layout: default` block if missing) so Jekyll renders it with the theme.
- The dropdown behaviour lives in `assets/js/measurement-switch.js`, written by
  the importer — do not edit it by hand.
