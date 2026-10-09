# TSV Wolnzach Scheduling

Automates the TSV Wolnzach basketball club's schedule handling, run as three steps via a
single CLI (`run_pipeline.py`):

1. **fetch** - logs into basketball-bund.net (TeamSL) with Selenium, scrapes every team's
   fixture list, and refreshes the local MySQL database (`spielplanung`).
2. **reports** - builds `planningTable.xlsx` (a day-by-team overview used to plan hall
   slots, with weekends/school holidays/blocked tournament dates highlighted), plus
   `GSP.xlsx` (full schedule, colour-coded per team) and `KG.xlsx` (Kampfgericht /
   scorer's-table duty roster).

This is a single-machine pipeline: it expects a MySQL server and a synced Google Drive
folder on the machine it runs on. There is no server/cloud component.

## Project layout

```
pipeline/
  settings.py        # secrets (.env) + season config (dates, holidays, events)
  db.py               # MySQL connection handling, shared by every step
  teams.py            # team tables, league URLs, opponent-name abbreviations, colours
  kampfgericht.py      # hand-curated scorer's-table duty assignments
  scraper.py          # "fetch" step logic
  excel_planning.py   # planning-table report logic
  excel_gsp.py         # GSP/KG report logic
  logging_utils.py

run_pipeline.py   # single CLI entry point for all steps
```

## Setup (one-time)

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your real TeamSL login and MySQL password.
   `.env` is gitignored - it never gets committed.
3. Make sure your local MySQL server (`spielplanung` database) and your Google Drive
   folder (`G:\My Drive\Spielplanung` by default, override via `OUTPUT_DIR` in `.env`)
   are available.

## Running

In your batch script (or interactively), call the single CLI once per step:

```
python run_pipeline.py fetch     # scrape + refresh MySQL
python run_pipeline.py reports   # rebuild planningTable.xlsx + GSP.xlsx + KG.xlsx
python run_pipeline.py all       # both, in order (fetch, then reports)
```

## Notes

- `KampfgerichtZuteilung.py` and `config.py` are kept as thin backwards-compatible shims
  pointing at `pipeline/kampfgericht.py` and `pipeline/settings.py`, in case anything else
  still imports them directly.
- Season dates, holidays and blocked tournament dates are edited directly in
  `pipeline/settings.py` once per season.
