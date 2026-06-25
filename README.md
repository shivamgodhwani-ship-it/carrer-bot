# Career Bot — AI-Powered Internship Assistant

An end-to-end internship automation pipeline built with Python, Playwright, and OpenRouter (LLM API). Scrapes listings, scores them against your profile using AI, tailors your resume per role, and auto-applies — with a Flask dashboard to track everything.

Built by [Shivam Godhwani](https://shivamgodhwani-ship-it.github.io/shivam-s-resume/) as a personal productivity tool and portfolio project.

---

## What it does

| Step | Module | What happens |
|------|--------|-------------|
| 1 | `job_finder.py` | Scrapes Internshala across 4 locations using Playwright |
| 2 | `scorer.py` | Scores each listing 1–10 via LLM; saves only those ≥8 |
| 3 | `resume_tailor.py` | Generates ATS-optimised bullet points per role |
| 4 | `apply_bot.py` | Auto-fills and submits applications via Playwright CDP; screenshots every submission |
| — | `dashboard.py` | Flask REST API + UI to track all applications and statuses |

Run everything in sequence with `python main.py`, or run each module individually.

---

## Stack

- **Python 3.10+**
- **Playwright** — browser automation for scraping and auto-apply
- **OpenRouter API** — LLM inference (GPT-3.5-turbo) for scoring, tailoring, and answer generation
- **Flask + Flask-CORS** — local dashboard backend
- **SQLite-ready** — application log stored as JSON, easy to migrate

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/career-bot.git
cd career-bot

# 2. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 3. Add your API key
cp .env.example .env
# Open .env and add your OpenRouter API key

# 4. Set your profile
# Create profile.json with your details (see profile.example.json)

# 5. Run
python main.py
```

---

## Auto-apply setup (Internshala)

The bot connects to a running Chrome instance via Chrome DevTools Protocol (CDP), so you stay logged in with your real session — no credentials stored anywhere.

```bash
# Step 1: Launch Chrome with debugging enabled
launch_chrome.bat          # Windows
# or manually:
# chrome --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug"

# Step 2: Log into Internshala in that Chrome window

# Step 3: Run the apply bot
python apply_bot.py
```

Screenshots of every application (before submit) are saved to `screenshots/`.

---

## Dashboard

```bash
launch_dashboard.bat       # Windows
# or: python dashboard.py
```

Opens at `http://localhost:5000` — shows scraped count, qualified jobs, applied/failed stats, and per-job status with screenshot previews.

---

## Project structure

```
career_bot/
├── main.py               # Runs all steps in sequence
├── job_finder.py         # Playwright scraper (Internshala)
├── scorer.py             # LLM-based relevance scoring
├── resume_tailor.py      # Per-role resume optimisation
├── apply_bot.py          # Auto-apply via Playwright CDP
├── resume_parser.py      # PDF resume extraction + parsing
├── job_pipeline.py       # Modular pipeline (find → score → tailor)
├── dashboard.py          # Flask backend for tracking UI
├── answers.json          # Fallback answers for common questions
├── requirements.txt
├── .env.example
├── launch_chrome.bat     # Windows helper to start Chrome
└── launch_dashboard.bat  # Windows helper to start dashboard
```

---

## Configuration

`answers.json` contains pre-written answers for standard application questions (availability, motivation, experience). The bot uses these as fallbacks; for custom questions it generates answers via LLM using your profile context.

Edit `PROFILE_CONTEXT` in `apply_bot.py` to match your background.

---

## Notes

- This tool is built for personal use. Respect platform terms of service.
- Auto-apply is opt-in; every application is screenshot-logged before submission.
- No credentials are stored. The CDP connection uses your existing browser session.
