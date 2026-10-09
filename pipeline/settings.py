"""
Centralised configuration for the pipeline.

Secrets (DB password, TeamSL login credentials) are loaded from a local ``.env`` file
(copy ``.env.example`` to ``.env`` and fill in your own values) so they never have to be
committed to git in plain text.

Everything that is *not* a secret - the current season's planning window, public/school
holidays, blocked tournament dates - stays as plain Python constants below. Those values
need to be edited by hand once per season anyway, so a config file would add no value.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

# Load key=value pairs from a .env file in the project root (if one exists) into the
# process environment. Real deployments (e.g. CI) can also just set env vars directly.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _require_env(name: str) -> str:
    """Reads a required environment variable, failing fast with a helpful message."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable '{name}'. "
            "Copy .env.example to .env in the project root and fill in your credentials."
        )
    return value


@dataclass(frozen=True)
class Settings:
    """Secrets and machine-specific paths, loaded once at import time."""

    # TeamSL (basketball-bund.net) login used by fetchSchedule.py
    teamsl_username: str
    teamsl_password: str
    login_url: str

    # Local MySQL connection used by every script
    db_host: str
    db_user: str
    db_password: str
    db_name: str

    # Google Drive folder the finished Excel reports are written to
    output_dir: Path


def _load_settings() -> Settings:
    return Settings(
        teamsl_username=_require_env("TEAMSL_USERNAME"),
        teamsl_password=_require_env("TEAMSL_PASSWORD"),
        login_url=os.getenv(
            "TEAMSL_LOGIN_URL", "https://www.basketball-bund.net/login.do?reqCode=showLogin"
        ),
        db_host=os.getenv("DB_HOST", "localhost"),
        db_user=os.getenv("DB_USER", "root"),
        db_password=_require_env("DB_PASSWORD"),
        db_name=os.getenv("DB_NAME", "spielplanung"),
        output_dir=Path(os.getenv("OUTPUT_DIR", r"G:\My Drive\Spielplanung")),
    )


# Imported by every other module as `from pipeline.settings import SETTINGS`.
SETTINGS = _load_settings()

# -----------------------------------------------------------------------------------------
# Season planning window
# -----------------------------------------------------------------------------------------
BZ_FIRST = date(2026, 9, 12)
BZ_LAST = date(2027, 4, 30)
RGL_FIRST = date(2026, 9, 25)
RGL_LAST = date(2027, 4, 11)

_season_dates = sorted([BZ_FIRST, BZ_LAST, RGL_FIRST, RGL_LAST])

# The planning table shows one extra week before/after the season so bye weeks and
# pre-/post-season friendlies can still be planned.
PLANNING_START = _season_dates[0] - timedelta(days=7)
PLANNING_END = _season_dates[-1] + timedelta(days=7)

# -----------------------------------------------------------------------------------------
# Tournaments / other events that block hall availability.
# Value is [date_string, duration_in_days] or [date_string, "HH:MM"] for a single time slot.
# -----------------------------------------------------------------------------------------
ADDITIONAL_EVENTS: dict[str, list] = {
    "Fußballturnier1": ["2027-01-15", 3],
    "Fußballturnier2": ["2027-01-22", 3],
    "Volleyballturnier": ["2025-01-18", 1],
    "MiniturnierU10": ["2026-12-06", "10:00"],
    "MiniturnierU12": ["2026-12-06", "13:00"],
}

# -----------------------------------------------------------------------------------------
# Bavarian national / school holidays that fall within the planning window.
# -----------------------------------------------------------------------------------------
HOLIDAYS = [
    "2026-10-31",
    "2026-11-07",
    "2026-12-26",
    "2027-01-02",
    "2027-01-09",
    "2027-02-06",
    "2027-02-13",
    "2027-03-20",
    "2027-03-27",
    "2027-04-03",
]
