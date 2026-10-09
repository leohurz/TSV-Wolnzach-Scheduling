"""
TSV Wolnzach scheduling pipeline.

This package contains all shared logic used by the three runnable entry-point
scripts in the project root:

    fetchSchedule.py       -> scrapes basketball-bund.net and refreshes MySQL
    createPlanningTable.py -> builds the team-vs-day planning Excel sheet
    send2excel.py          -> builds the GSP / Kampfgericht (KG) Excel sheets

Everything here is designed to run on a single machine (your local MySQL
server + Google Drive folder) - there is no server/deployment component.
"""
