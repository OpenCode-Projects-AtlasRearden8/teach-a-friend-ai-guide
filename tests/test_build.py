"""Build and content tests for Teach a Friend AI.

Run with:
    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import functools
import http.server
import re
import threading
import unittest
import urllib.request
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import build as buildmod

ROOT = Path(buildmod.ROOT)
DOCS = ROOT / "docs"
SITE = ROOT / "site"

EXPECTED_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"

ALL_DOC_PATHS = [ROOT / d for d, _ in buildmod.TOC_TITLES]
TEXT_SUFFIXES = {".md", ".py", ".css", ".txt"}
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",
    r"eyJ[A-Za-z0-9_-]{20,}",
    r"(?i)api[_-]?key['\"]?\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
    r"(?i)password\s*[:=]\s*['\"]?[A-Za-z0-9!@#$%^&*]{8,}",
]


def repo_text_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if "site" in path.parts or "__pycache__" in path.parts:
            continue
        yield path


class TestMarkdownManual(unittest.TestCase):
    def test_all_chapters_exist(self):
        self.assertGreaterEqual(len(ALL_DOC_PATHS), 9)
        for path in ALL_DOC_PATHS:
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_every_chapter_has_opening_heading(self):
        for path in ALL_DOC_PATHS:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.lstrip().startswith("# "), f"{path.name} lacks an H1")

    def test_internal_links_resolve(self):
        known = {p.relative_to(ROOT) for p in ALL_DOC_PATHS}
        for path in ALL_DOC_PATHS:
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\((?!https?://)([^)#]+?\.md)(?:#[^)]*)?\)", text):
                resolved = (path.parent / target).relative_to(ROOT)
                self.assertIn(resolved, known, f"broken link in {path.name}: {target}")

    def test_core_topics_covered(self):
        required = {
            "05-run-the-session.md": "minute",
            "06-celebrate-and-continue.md": "wins journal",
            "07-hand-off-safely.md": "handoff conversation",
            "08-scripts-and-cheat-sheets.md": "not that",
        }
        for name, needle in required.items():
            text = (DOCS / name).read_text(encoding="utf-8").lower()
            self.assertIn(needle.lower(), text, f"topic missing from {name}")

    def test_pacing_chapter_covers_everybody(self):
        pacing = (DOCS / "04-pace-for-the-learner.md").read_text(encoding="utf-8")
        for learner in ("The senior", "The skeptical spouse", "The student",
                        "The busy friend", "The self-taught dabbler"):
            self.assertIn(learner, pacing)

    def test_distinct_positioning_from_sibling_projects(self):
        index_text = (DOCS / "index.md").read_text(encoding="utf-8")
        self.assertIn("not a curriculum, not tech support", index_text.replace("**", ""))
        self.assertIn("one friend, one hour at a time", index_text.replace("*", ""))


class TestGeneratedSite(unittest.TestCase):
    site_pages = []

    @classmethod
    def setUpClass(cls):
        buildmod.build(clean=True)
        cls.site_pages = sorted(SITE.glob("*.html"))

    def test_all_pages_built(self):
        self.assertEqual(len(self.site_pages), 9)

    def test_pages_share_navigation_and_credit(self):
        for page in self.site_pages:
            text = page.read_text(encoding="utf-8")
            self.assertIn('aria-current="page"', text, page.name)
            self.assertIn("Asdale Dynamics, LLC", text, page.name)
            self.assertIn('rel="stylesheet" href="style.css"', text, page.name)

    def test_nav_links_resolve_in_site(self):
        names = {p.name for p in self.site_pages} | {"style.css"}
        for page in self.site_pages:
            html = page.read_text(encoding="utf-8")
            for href in re.findall(r'href="([a-zA-Z0-9][^"]*)"', html):
                if href.startswith(("data:", "http", "#")):
                    continue
                target = href.split("#")[0]
                if not target:
                    continue
                self.assertIn(Path(target).name, names,
                              f"dangling site link {href} in {page.name}")

    def test_no_raw_md_links_left_in_html(self):
        for page in self.site_pages:
            self.assertNotRegex(page.read_text(encoding="utf-8"),
                                r'href="[^"]*\.md"', page.name)

    def test_nav_covers_all_chapters(self):
        index_html = (SITE / "index.html").read_text(encoding="utf-8")
        for page in self.site_pages:
            self.assertIn(f'href="{page.name}"', index_html, page.name)


class TestRepoHousekeeping(unittest.TestCase):
    def test_license_line_exact(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License"))
        self.assertIn(EXPECTED_COPYRIGHT, license_text)

    def test_readme_credits_llc(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("MIT", readme)

    def test_no_secrets_or_personal_data(self):
        for path in repo_text_files():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                self.assertNotRegex(text, pattern, f"possible secret in {path}")


class TestSiteServesOverHttp(unittest.TestCase):
    def test_site_serves(self):
        import socket

        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]

        handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                    directory=str(SITE))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{port}"
        try:
            with urllib.request.urlopen(f"{base}/index.html", timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode("utf-8")
            self.assertIn("Teach a Friend AI", body)
            for name in ("01-the-heart-of-helping.html", "08-scripts-and-cheat-sheets.html"):
                with urllib.request.urlopen(f"{base}/{name}", timeout=5) as resp:
                    self.assertEqual(resp.status, 200)
            with urllib.request.urlopen(f"{base}/style.css", timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                self.assertTrue(resp.headers["Content-Type"].startswith("text/css"))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
