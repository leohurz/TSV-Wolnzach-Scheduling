"""Backwards-compatible shim.

All configuration now lives in `pipeline/settings.py` (secrets are loaded from a local
`.env` file - see `.env.example`). This module just re-exports the same names so any
old code/notebooks importing `config.xxx` keep working unchanged.
"""
from pipeline.settings import (  # noqa: F401
    ADDITIONAL_EVENTS as additional_events,
    HOLIDAYS as Holidays,
    PLANNING_END as end,
    PLANNING_START as start,
    SETTINGS,
)

username = SETTINGS.teamsl_username
password = SETTINGS.teamsl_password
login_url = SETTINGS.login_url
