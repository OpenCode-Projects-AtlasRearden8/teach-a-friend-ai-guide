# Teach a Friend AI — A Warm Manual for Being the Helper

*One friend, one hour at a time. A manual by [Asdale Dynamics, LLC](https://dylanasdale.github.io).*

You already use AI. Someone in your life has noticed — a parent, a spouse, a
roommate, a friend who keeps saying "I should learn that someday." This manual
is for **you**, the person holding the door open. Not a class, not tech
support: **one friend, one hour at a time.**

It covers how to run kind, low-pressure one-on-one sessions; how to pick the
first real task that makes it click; how to pace for different learners
(seniors, skeptical spouses, students, busy friends, self-taught dabblers);
how to celebrate real wins without being condescending; and how to hand off
safely, so you're not their AI helper forever.

**Distinct from the family-tech-support job** (fixing the household's
printers and Wi-Fi) **and from the community-class job** (teaching a room of
strangers). This is the couch, the laptop, one task, and an hour.

## What's inside

| Chapter | Topic |
|---|---|
| [Welcome](docs/index.md) | Who this is for and the arc of a full helping run |
| [1. The Heart of Helping](docs/01-the-heart-of-helping.md) | Patience over pride, curiosity over correction, dignity always |
| [2. Prepare the Hour](docs/02-prepare-the-hour.md) | Setup checklist, the password-and-privacy moment |
| [3. Pick the First Real Task](docs/03-pick-the-first-real-task.md) | The task picker, reliable openers, trap tasks to avoid |
| [4. Pace for the Learner](docs/04-pace-for-the-learner.md) | Seniors, skeptics, students, busy friends, dabblers |
| [5. Run the Session](docs/05-run-the-session.md) | The minute-by-minute shape of one golden hour |
| [6. Celebrate and Continue](docs/06-celebrate-and-continue.md) | Wins journal, between-session rhythm, sessions 2–6 |
| [7. Hand Off Safely](docs/07-hand-off-safely.md) | The handoff conversation, privacy hygiene, happy endings |
| [8. Scripts and Cheat Sheets](docs/08-scripts-and-cheat-sheets.md) | Say-this-not-that, one-pagers, hard-question scripts |

## How to run the site

Requirements: Python 3.10+ with the `markdown` package
(`pip install markdown`).

```bash
# Build the static HTML site from the Markdown manual
python3 build.py            # outputs to site/ (add --clean to start fresh)

# View it: open site/index.html directly in a browser, or serve it:
python3 -m http.server 8321 --directory site
# then visit http://localhost:8321/
```

Run the tests (build + link checks + content checks + a live server smoke
test):

```bash
python3 -m unittest discover -s tests -v
```

## The one rule everything hangs on

> **Never make the person feel dumb.** Not in your words, not in your pauses,
> not in how fast you reach for the keyboard.

Everything in the manual is built to keep that promise.

## Scope and safety

This manual is **education only** — it is never medical, legal, or financial
advice. It teaches friends to help friends learn AI tools. It includes no
product keys, accounts, or personal data, and it works fully offline once
downloaded (the site is plain static HTML).

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC, founded by Dylan Asdale (a registered nurse turned AI
author, author of *The Massive AI Manual*), makes beginner-friendly AI
education: books, guides, and practical tools explained "like a friend
would" — plain English, step by step, never condescending. Hub:
<https://dylanasdale.github.io>

## License

MIT — see [LICENSE](LICENSE). © Asdale Dynamics, LLC, 2026. Print it, share
it, use it with someone you love.
