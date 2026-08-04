#!/usr/bin/env python3
"""Check the built Jekyll site for problems that fail silently.

Jekyll does not error on any of these -- a broken page just quietly 404s on
the live site -- so they are only caught by looking at the build output.

  1. Pages that did not render. Jekyll only converts a .md file to .html when
     it begins with a YAML front matter block. A missing block, or a UTF-8 BOM
     sitting in front of it, makes Jekyll treat the file as a static asset and
     copy it through as raw .md.
  2. Page-to-page links pointing at .html files the build never produced.
  3. Navigation links in _config.yml pointing at pages that do not exist.

Run after `bundle exec jekyll build`:

    python script/check_site.py [--site _site]

Exits non-zero if anything is wrong.
"""

import argparse
import glob
import os
import re
import sys

import yaml

# Root-level markdown that documents the repo rather than being a wiki page.
# These are expected to stay unrendered.
NON_PAGE_MARKDOWN = {
    "README.md",
    "SETUP.md",
    "QUICK_START.md",
    "DEPLOYMENT_CHECKLIST.md",
    "POWER_MEASUREMENTS.md",
}

BOM = b"\xef\xbb\xbf"

# [text](target) with an optional "title". Skips images -- the leading ! is
# not matched, but a preceding char is not checked, so ![x](y) still parses as
# a link; harmless, since we only inspect .html targets.
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")

EXTERNAL_RE = re.compile(r"^(https?:|mailto:|ftp:|//|#)")


def markdown_sources(root):
    """Every .md file that should become a page, repo-relative, posix style."""
    out = []
    for path in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith("_site/") or rel.startswith("vendor/"):
            continue
        if rel in NON_PAGE_MARKDOWN:
            continue
        out.append(rel)
    return sorted(out)


def check_front_matter(root, sources):
    """Find pages Jekyll will not render, and say which of the two causes it is."""
    problems = []
    for rel in sources:
        with open(os.path.join(root, rel), "rb") as fh:
            head = fh.read(512)
        if head.startswith(BOM):
            problems.append(
                (rel, "starts with a UTF-8 BOM before the front matter "
                      "(save as UTF-8 without BOM)"))
        elif not head.startswith(b"---"):
            problems.append(
                (rel, "has no YAML front matter (needs a --- block with "
                      "layout and title as the very first bytes)"))
    return problems


def check_rendered(root, site, sources):
    """Confirm each source page actually produced an .html file."""
    problems = []
    for rel in sources:
        expected = os.path.join(site, rel[:-3] + ".html")
        if not os.path.exists(os.path.join(root, expected)):
            problems.append((rel, "did not render to " + rel[:-3] + ".html"))
    return problems


def built_pages(root, site):
    """Site-root-relative .html paths, lowercased for case-insensitive lookup."""
    site_dir = os.path.join(root, site)
    pages = set()
    for path in glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True):
        rel = os.path.relpath(path, site_dir).replace(os.sep, "/")
        pages.add(rel.lower())
    return pages


def check_links(root, sources, pages, baseurl):
    """Find relative page-to-page links with no corresponding built page."""
    problems = []
    for rel in sources:
        base = os.path.dirname(rel)
        with open(os.path.join(root, rel), encoding="utf-8") as fh:
            text = fh.read()
        for label, href in LINK_RE.findall(text):
            if EXTERNAL_RE.match(href):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target.endswith(".html"):
                continue
            if target.startswith("/"):
                # Site-absolute: strip the configured baseurl to get a site path.
                path = target[1:]
                if baseurl and path.lower().startswith(baseurl.lower() + "/"):
                    path = path[len(baseurl) + 1:]
            else:
                path = os.path.normpath(os.path.join(base, target))
            path = path.replace(os.sep, "/")
            if path.lower() not in pages:
                label = " ".join(label.split())[:40]
                problems.append((rel, "link [%s](%s) has no such page" % (label, href)))
    return problems


def check_nav(root, pages, baseurl):
    """Check the sidebar links in _config.yml, which appear on every page."""
    with open(os.path.join(root, "_config.yml"), encoding="utf-8") as fh:
        config = yaml.safe_load(fh)

    problems = []

    def visit(entries):
        for entry in entries or []:
            link = entry.get("link")
            if link and not EXTERNAL_RE.match(link):
                path = link.split("#")[0].lstrip("./")
                if path.startswith("/"):
                    path = path[1:]
                if baseurl and path.lower().startswith(baseurl.lower() + "/"):
                    path = path[len(baseurl) + 1:]
                if path.endswith(".html") and path.lower() not in pages:
                    problems.append(
                        ("_config.yml", "nav entry %r links to missing %s"
                         % (entry.get("name", "?"), link)))
            visit(entry.get("sublist"))

    visit(config.get("navigation"))
    return problems


def report(title, problems):
    if not problems:
        return 0
    print("\n%s (%d):" % (title, len(problems)))
    for where, detail in problems:
        print("  %s: %s" % (where, detail))
    return len(problems)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default="_site",
                        help="build output directory (default: _site)")
    parser.add_argument("--root", default=".", help="repository root")
    args = parser.parse_args()

    root = args.root
    site_dir = os.path.join(root, args.site)
    if not os.path.isdir(site_dir):
        sys.exit("error: %s not found -- run 'bundle exec jekyll build' first"
                 % site_dir)

    with open(os.path.join(root, "_config.yml"), encoding="utf-8") as fh:
        baseurl = (yaml.safe_load(fh).get("baseurl") or "").strip("/")

    sources = markdown_sources(root)
    pages = built_pages(root, args.site)

    # A page missing front matter also fails the rendered check; report the
    # front matter cause and suppress the redundant follow-on.
    fm = check_front_matter(root, sources)
    broken_sources = {rel for rel, _ in fm}
    unrendered = [p for p in check_rendered(root, args.site, sources)
                  if p[0] not in broken_sources]

    total = 0
    total += report("Pages Jekyll will not render", fm)
    total += report("Pages missing from the build", unrendered)
    total += report("Broken internal links", check_links(root, sources, pages, baseurl))
    total += report("Broken navigation links", check_nav(root, pages, baseurl))

    print()
    if total:
        print("FAIL: %d problem(s) found across %d page(s)." % (total, len(sources)))
        return 1
    print("OK: %d pages, all rendered with valid internal links." % len(sources))
    return 0


if __name__ == "__main__":
    sys.exit(main())
