# STATUS.md — Teach a Friend AI

_Last updated: 2026-11-06_

## What was built

**Teach a Friend AI** is a warm, substantive manual on being the AI helper:
run kind one-on-one sessions, pick the first real task, pace for different
learners, celebrate wins, and hand off safely. One friend, one hour at a time
— deliberately distinct from household tech-support guides and from
community-class kits.

### Contents

- `docs/index.md` — welcome page: who this is for, the 4–6 session arc
- `docs/01-the-heart-of-helping.md` — mindset: patience over pride,
  curiosity over correction, "never make the person feel dumb"
- `docs/02-prepare-the-hour.md` — session prep checklist, the
  password-and-privacy moment done right from day one
- `docs/03-pick-the-first-real-task.md` — the six-part definition of a Real
  First Task, a task picker keyed to learner answers, veteran openers,
  trap tasks to avoid, the "click" moment
- `docs/04-pace-for-the-learner.md` — pacing maps for seniors, skeptical
  spouses, students, busy friends, and self-taught dabblers
- `docs/05-run-the-session.md` — the minute-by-minute shape of one golden
  hour (00–05 arrive, 05–10 demo, 10–40 first task, 40–50 explore,
  50–60 write + celebrate + stop on time), plus a wobble menu
- `docs/06-celebrate-and-continue.md` — output wins vs. move wins, how to
  celebrate without condescension, the wins journal, between-session
  rhythm, the sessions 2–6 spiral
- `docs/07-hand-off-safely.md` — the "it's time" checklist, the ten-minute
  handoff conversation, permission slips and happy landing states, privacy
  hygiene for both sides, and the mirror case (they teach you)
- `docs/08-scripts-and-cheat-sheets.md` — say-this-not-that table, session
  openers, rescue lines, printable one-pagers (fridge cheat sheet, helper's
  session card, wins journal), and scripts for hard questions
- `site/` — the generated static HTML site (9 pages + `style.css`),
  self-contained plain HTML with no scripts, no secrets, no personal data
- `build.py` — Python build script: converts `docs/*.md` to `site/*.html`
  (python-markdown, shared nav, task-list checkboxes, rewritten links)
- `tests/test_build.py` — 15 unittest cases (see Verification)
- `README.md` — overview, run instructions, LLC credit
- `LICENSE` — MIT, copyright line exactly: `Copyright (c) 2026 Asdale
  Dynamics, LLC`

## How to run it

Requires Python 3.10+ and the `markdown` package (`pip install markdown`).

```bash
# Build the static site
python3 build.py            # add --clean to wipe site/ first

# View: open site/index.html in a browser, or
python3 -m http.server 8321 --directory site
# then visit http://localhost:8321/

# Run the test suite
python3 -m unittest discover -s tests -t . -v
```

## Verification results

All of the following were run locally and passed on 2026-11-06:

- `python3 build.py --clean` → "Built 9 pages + style.css into site/
  (83,099 bytes)"; all 9 pages + `style.css` present.
- `python3 -m unittest discover -s tests -t .` → **Ran 15 tests … OK**,
  including:
  - all 9 markdown chapters exist and carry an H1
  - internal markdown links resolve to real chapters
  - core topics present (session shape, wins journal, handoff, scripts)
  - pacing chapter covers all five learner types
  - generated pages all ship shared nav, the Asdale Dynamics, LLC credit,
    and no dangling or raw `.md` links
  - LICENSE line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`;
    README credits Asdale Dynamics, LLC
  - no secrets / API keys / personal data patterns in any text file
  - live smoke test: the site serves over HTTP (index, two chapters,
    style.css all 200)
- Manual live check: `python3 -m http.server 8321 --directory site` +
  curl → 200 for index, two chapters, and style.css.

## Known gaps

- Learner archetypes could each use their own worked example dialogue
  (transcripts of a full first session per type).
- The site is one style; a print/print-PDF stylesheet for the one-pagers
  (Chapter 8) would make them nicer to hand over on paper.
- No per-chapter audio version (useful for seniors) — text only for now.
- The wins journal is printable text; a fillable template file and/or a
  blank-PDF would be a small extra.
- Tests cover structure, links, and serving; they cannot judge tone. The
  manual's warmth is human-reviewed, not test-reviewed.
- `site/` is committed for convenience (browse without building), so it
  needs a `python3 build.py --clean` after content edits.

## Credit

Written and published by **Asdale Dynamics, LLC** (Dylan Asdale,
dylanasdale.github.io). MIT licensed; no secrets, no personal data.
