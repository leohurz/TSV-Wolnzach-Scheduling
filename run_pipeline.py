"""
Single CLI entry point that runs the full pipeline, or any individual step.

Examples
--------
    python run_pipeline.py fetch              # scrape + refresh MySQL only
    python run_pipeline.py reports            # rebuild both Excel reports only
    python run_pipeline.py all                # fetch, then rebuild both reports
"""
from __future__ import annotations

import argparse
import logging

from pipeline.logging_utils import configure_logging

logger = logging.getLogger(__name__)


def run_fetch() -> None:
    from pipeline.scraper import run as fetch_schedules

    fetch_schedules()


def run_planning_table() -> None:
    from pipeline.excel_planning import run as build_planning_table

    build_planning_table()


def run_gsp_reports() -> None:
    from pipeline.excel_gsp import run as build_gsp_reports

    build_gsp_reports()


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(description="TSV Wolnzach scheduling pipeline")
    parser.add_argument(
        "step",
        choices=["fetch", "reports", "all"],
        help=(
            "'fetch' scrapes schedules into MySQL, 'reports' rebuilds the planning table "
            "+ GSP/KG Excel exports from the current MySQL data, 'all' does both in order"
        ),
    )
    args = parser.parse_args()

    if args.step in ("fetch", "all"):
        logger.info("Step: fetch schedules")
        run_fetch()

    if args.step in ("reports", "all"):
        logger.info("Step: build planning table")
        run_planning_table()
        logger.info("Step: build GSP/KG reports")
        run_gsp_reports()

    logger.info("Done!")


if __name__ == "__main__":
    main()
