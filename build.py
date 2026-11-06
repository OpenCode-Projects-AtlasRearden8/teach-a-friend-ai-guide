#!/usr/bin/env python3
"""Build the static HTML site from the Markdown manual in docs/.

Usage: python3 build.py [--clean]

The generated site is written to site/ (self-contained HTML pages plus
style.css). Each docs/*.md page becomes one site/*.html page with shared
navigation, and internal Markdown links are resolved to .html counterparts.

Copyright (c) 2026 Asdale Dynamics, LLC
MIT License
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

MD_EXTENSIONS = ["tables", "toc", "fenced_code", "sane_lists"]
MD_CONFIG = {"toc": {"permalink": False}}

TOC_TITLES = [
    ("docs/index.md", "Welcome"),
    ("docs/01-the-heart-of-helping.md", "1. The Heart of Helping"),
    ("docs/02-prepare-the-hour.md", "2. Prepare the Hour"),
    ("docs/03-pick-the-first-real-task.md", "3. Pick the First Real Task"),
    ("docs/04-pace-for-the-learner.md", "4. Pace for the Learner"),
    ("docs/05-run-the-session.md", "5. Run the Session"),
    ("docs/06-celebrate-and-continue.md", "6. Celebrate and Continue"),
    ("docs/07-hand-off-safely.md", "7. Hand Off Safely"),
    ("docs/08-scripts-and-cheat-sheets.md", "8. Scripts and Cheat Sheets"),
]

CREDIT = "Asdale Dynamics, LLC"


def page_relative_links(text: str) -> str:
    """Rewrite internal .md links (with optional anchors) to .html links."""
    def repl(match: re.Match) -> str:
        target, anchor = match.group(1), match.group(2) or ""
        if re.match(r"https?://", target):
            return match.group(0)
        html_target = re.sub(r"\.md$", ".html", target)
        return f"({html_target}{anchor})"

    return re.sub(r"\(([^()]*?\.md)(#[^()]*)?\)", repl, text)


def relative_doc_path(doc_path: Path) -> str:
    return str(doc_path.relative_to(ROOT)).replace("\\", "/")


def md_to_html_page(doc_path: Path) -> tuple[str, str, str]:
    """Convert one docs markdown file to (title, nav_html, body_html)."""
    raw = doc_path.read_text(encoding="utf-8")
    raw = page_relative_links(raw)
    md = markdown.Markdown(
        extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG
    )
    body = md.convert(raw)
    body = body.replace("<li>[ ]", '<li class="task"><span aria-hidden="true">☐</span>')
    body = body.replace("<li>[x]", '<li class="task done"><span aria-hidden="true">☑</span>')

    title_match = re.match(r"^#\s+(.+)$", raw.lstrip(), flags=re.MULTILINE)
    title = html.escape(title_match.group(1).strip()) if title_match else "Teach a Friend AI"

    current = relative_doc_path(doc_path)
    nav_items = []
    for doc_ref, label in TOC_TITLES:
        href = re.sub(r"^docs/(.+)\.md$", r"\1.html", doc_ref)
        display = html.escape(label)
        if doc_ref == current:
            nav_items.append(f'<li><a href="{href}" aria-current="page">{display}</a></li>')
        else:
            nav_items.append(f'<li><a href="{href}">{display}</a></li>')
    nav = "\n        ".join(nav_items)
    return title, nav, body


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Teach a Friend AI</title>
<meta name="description" content="A warm, practical manual for helping one friend learn AI, one hour at a time. By Asdale Dynamics, LLC.">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='0.9em' font-size='90'%3E%F0%9F%A4%9D%3C/text%3E%3C/svg%3E">
</head>
<body>
<nav class="site-nav">
  <a class="site-title" href="index.html"><strong>Teach a Friend AI</strong><span class="tagline">one friend, one hour at a time</span></a>
  <ul class="nav-list">
        {nav}
  </ul>
  <p class="nav-credit">A manual by {credit}</p>
</nav>
<main class="content">
{body}
</main>
<footer class="site-footer">
  <p>Teach a Friend AI — © {credit}, 2026. Open source under the <a href="https://opensource.org/licenses/MIT" rel="license">MIT License</a>. This guide is education only; it is never medical, legal, or financial advice.</p>
</footer>
</body>
</html>
"""

STYLE = """\
:root {
  --bg: #fdf9f4;
  --paper: #ffffff;
  --ink: #2c2a26;
  --muted: #6f6a60;
  --accent: #c2622d;
  --accent-soft: #f4e3d5;
  --line: #e6ddcf;
}

* { box-sizing: border-box; }

body {
  margin: 0 auto;
  max-width: 60em;
  display: grid;
  grid-template-columns: 16.5em 1fr;
  gap: 2.5rem;
  padding: 2rem 1.25rem 4rem;
  font-family: Georgia, "Times New Roman", serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.65;
}

.site-nav {
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: 0.92rem;
  position: sticky;
  top: 2rem;
  align-self: start;
}

.site-title {
  display: block;
  color: var(--ink);
  text-decoration: none;
  font-size: 1.2rem;
  line-height: 1.3;
  margin-bottom: 0.25rem;
}

.site-title .tagline {
  display: block;
  color: var(--muted);
  font-size: 0.85rem;
  font-style: italic;
}

.nav-list { list-style: none; margin: 1rem 0 0.75rem; padding: 0; }
.nav-list li { margin: 0; }
.nav-list a {
  display: block;
  color: var(--ink);
  text-decoration: none;
  padding: 0.3rem 0.6rem;
  border-left: 3px solid transparent;
}
.nav-list a:hover { background: var(--accent-soft); }
.nav-list a[aria-current="page"] {
  border-left-color: var(--accent);
  font-weight: 600;
  background: var(--accent-soft);
}

.nav-credit { color: var(--muted); font-size: 0.8rem; padding-left: 0.6rem; }

.content { min-width: 0; }

.content h1, .content h2, .content h3 { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.25; }
.content h1 { font-size: 2rem; border-bottom: 3px solid var(--accent); padding-bottom: 0.3rem; }
.content h2 { font-size: 1.4rem; margin-top: 2rem; }
.content h3 { font-size: 1.05rem; margin-top: 1.4rem; }

.content a { color: var(--accent); }
.content blockquote {
  margin: 1rem 0;
  padding: 0.4rem 1rem;
  border-left: 4px solid var(--accent);
  background: var(--paper);
  font-style: italic;
}
.content table { border-collapse: collapse; width: 100%; margin: 1rem 0; background: var(--paper); font-size: 0.95rem; }
.content th, .content td { border: 1px solid var(--line); padding: 0.45rem 0.7rem; text-align: left; vertical-align: top; }
.content th { background: var(--accent-soft); font-family: system-ui, sans-serif; font-size: 0.85rem; }
.content pre {
  background: #2c2a26;
  color: #f3efe7;
  padding: 1rem;
  overflow-x: auto;
  border-radius: 6px;
  line-height: 1.5;
}
.content code { font-family: "SFMono-Regular", Consolas, monospace; font-size: 0.9em; }
.content p > code, .content li > code { background: var(--accent-soft); padding: 0.1em 0.35em; border-radius: 3px; }
.content ul.checkbox-list input[type="checkbox"] { margin-right: 0.4rem; }
.content li.task { list-style: none; margin-left: -1.2em; margin-bottom: 0.4rem; }

.site-footer {
  grid-column: 2;
  border-top: 1px solid var(--line);
  margin-top: 3rem;
  padding-top: 1rem;
  color: var(--muted);
  font-size: 0.85rem;
}

@media (max-width: 50em) {
  body { display: block; padding: 1rem 0.9rem 4rem; }
  .site-nav { position: static; }
  .site-footer { margin-top: 2rem; }
}
"""


def build(clean: bool = False) -> list[Path]:
    if clean and SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(exist_ok=True)

    (SITE / "style.css").write_text(STYLE, encoding="utf-8")

    written: list[Path] = []
    doc_paths, missing = [], [d for d, _ in TOC_TITLES if not (ROOT / d).exists()]
    if missing:
        raise FileNotFoundError(f"missing docs listed in TOC_TITLES: {missing}")
    doc_paths = [ROOT / d for d, _ in TOC_TITLES]

    for doc in doc_paths:
        title, nav, body = md_to_html_page(doc)
        page = PAGE_TEMPLATE.format(title=title, nav=nav, body=body, credit=CREDIT)
        out = SITE / (doc.stem + ".html")
        out.write_text(page, encoding="utf-8")
        written.append(out)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="remove site/ before building")
    args = parser.parse_args(argv)
    pages = build(clean=args.clean)
    size = sum(p.stat().st_size for p in pages)
    print(f"Built {len(pages)} pages + style.css into site/ ({size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
