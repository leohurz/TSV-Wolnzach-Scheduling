"""Backwards-compatible shim.

The Kampfgericht (scorer's-table duty) assignments now live in
`pipeline/kampfgericht.py`. This module just re-exports the same dict under its old name
so any old code/notebooks importing `KampfgerichtZuteilung.kg` keep working unchanged.
"""
from pipeline.kampfgericht import KAMPFGERICHT_ASSIGNMENTS as kg  # noqa: F401
