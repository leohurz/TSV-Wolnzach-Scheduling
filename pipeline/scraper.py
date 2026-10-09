"""
Scrapes the TSV Wolnzach basketball schedule from basketball-bund.net (TeamSL) for every
configured team/league and syncs the results into the local MySQL database.

This is a straight refactor of the original script: same login flow, same page-scraping
approach (Selenium to log in and render the page, BeautifulSoup to parse it), same table
layout - just reorganised into small testable functions, with the outdated
``find_element_by_name(...)`` calls (removed in Selenium 4) replaced by the current
``find_element(By.NAME, ...)`` API, and prints replaced with logging.

Run directly: ``python fetchSchedule.py``
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

import bs4
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from pipeline import db
from pipeline.logging_utils import configure_logging
from pipeline.settings import SETTINGS
from pipeline.teams import LEAGUE_URLS, LEAGUES, TEAM_TABLES

logger = logging.getLogger(__name__)


@dataclass
class GameRecord:
    """One parsed schedule row, in the same column order as the MySQL team tables."""

    spnr: str
    spt: str
    team: str
    liga: str
    datum: str
    uhrzeit: str
    heim: str
    gast: str
    halle: str
    id: str

    def as_row(self) -> tuple:
        """Returns the record as a tuple matching ``pipeline.db.GAME_COLUMNS`` order."""
        return (
            self.spnr, self.spt, self.team, self.liga, self.datum,
            self.uhrzeit, self.heim, self.gast, self.halle, self.id,
        )


def build_driver() -> webdriver.Chrome:
    """Creates a headless Chrome driver (same options as the original script)."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--silent")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)


def login(driver: webdriver.Chrome) -> None:
    """Logs into the TeamSL portal using credentials from `.env`."""
    driver.get(SETTINGS.login_url)
    driver.find_element(By.NAME, "username").send_keys(SETTINGS.teamsl_username)
    driver.find_element(By.NAME, "password").send_keys(SETTINGS.teamsl_password)
    driver.find_element(
        By.CSS_SELECTOR, 'a.button[title="klicken Sie hier, um Sich anzumelden!"]'
    ).click()


def _parse_row(row: Tag, team_tag: str, liga: str) -> GameRecord | None:
    """Parses a single schedule table row.

    Returns ``None`` for rows that aren't an actual game: layout/header rows (where the
    first cell isn't plain text) and cancelled games (rendered with a <strike> tag instead
    of plain text in the date/time cell).
    """
    elements = row.select("nobr")
    raw_values = []
    for index in range(6):
        try:
            raw_values.append(elements[index].contents[0])
        except IndexError:
            raw_values.append("NaN")

    if not isinstance(raw_values[0], bs4.element.NavigableString):
        return None
    if isinstance(raw_values[2], Tag):
        return None

    spnr, spt, date_time, heim, gast, halle = raw_values
    date_str, time_str = date_time.split()

    datum = datetime.strptime(date_str.replace(".", "-"), "%d-%m-%Y").strftime("%Y-%m-%d")
    uhrzeit = f"{time_str}:00"
    game_id = f"{spnr}{team_tag}"

    return GameRecord(
        spnr=spnr, spt=spt, team=team_tag, liga=liga, datum=datum,
        uhrzeit=uhrzeit, heim=heim, gast=gast, halle=halle, id=game_id,
    )


def scrape_team_schedule(driver: webdriver.Chrome, data_url: str, team_tag: str, liga: str) -> list[GameRecord]:
    """Scrapes a single team's schedule page. The driver must already be logged in."""
    driver.get(data_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # the 3rd "sportView" table on the page holds the actual fixture list
    schedule_table = soup.select("table.sportView")[2]
    rows = schedule_table.select("tr")

    # skip header rows; some leagues show an extra "Bearbeiten" (edit) header row
    header_row_count = 9 if "Bearbeiten" in rows[8].text else 8
    rows = rows[header_row_count:]

    games = (_parse_row(row, team_tag, liga) for row in rows)
    return [game for game in games if game is not None]


def run() -> None:
    """Scrapes every configured team's schedule and refreshes its MySQL table."""
    configure_logging()
    driver = build_driver()
    try:
        login(driver)
        for team_tag, liga in zip(TEAM_TABLES, LEAGUES):
            data_url = LEAGUE_URLS.get(team_tag, "")
            if not data_url:
                logger.info("No schedule URL configured for '%s' - skipping", team_tag)
                continue

            try:
                games = scrape_team_schedule(driver, data_url, team_tag, liga)
                db.replace_team_games(team_tag, [game.as_row() for game in games])
                logger.info("%s: synced %d games", team_tag, len(games))
            except Exception:
                # one team's page failing (e.g. unexpected layout) shouldn't stop the rest
                logger.exception("Failed to sync team '%s' - continuing with the rest", team_tag)
    finally:
        driver.quit()

    logger.info("Schedule fetch complete")


if __name__ == "__main__":
    run()
