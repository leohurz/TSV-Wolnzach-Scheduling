from datetime import date, timedelta

# -----------------------------------------------------------------------------
# login
username = "212150"
password = "bbwoz"
login_url = "https://www.basketball-bund.net/login.do?reqCode=showLogin"

# ----------------------------------------------------------------------------
# planning Window
bz_first = date(2026, 9, 12)
bz_last = date(2027, 4, 30)
rgl_first = date(2026, 9, 25)
rgl_last = date(2027, 4, 11)

dates = [bz_first, bz_last, rgl_first,  rgl_last]
dates.sort()

start = dates[0] - timedelta(days=7)
end = dates[-1] + timedelta(days=7)

# -----------------------------------------------------------------------------
# Tournaments od other divisions

additional_events = {
    "Fußballturnier1": ["2027-01-15", 3],
    "Fußballturnier2": ["2027-01-22", 3],
    "Volleyballturnier": ["2025-01-18", 1],
    "MiniturnierU10": ["2026-12-06", "10:00"],
    "MiniturnierU12": ["2026-12-06", "13:00"]
}

# -------------------------------------------------------------------------------
# National Holidays

Holidays = ["2026-10-31",
            "2026-11-07",
            "2026-12-26",
            "2027-01-02",
            "2027-01-09",
            "2027-02-06",
            "2027-02-13",
            "2027-03-20",
            "2027-03-27",
            "2027-04-03"]

# ---------------------------------------------------------------------------------
# Kampfgericht?
print("stop")

