"""Evaluation utilities for KG-to-framework conversion quality."""

from __future__ import annotations

import sys
from pathlib import Path

# Make `kg_to_script/` (the parent of `src/`) importable as a path root so
# that `from src.core...` imports used throughout this package resolve
# regardless of the caller's cwd or invocation form (e.g. run from the repo
# root as `python -m kg_to_script.evaluation.run`, or from within
# `kg_to_script/` as `python -m evaluation.run`).
_kg_to_script_root = str(Path(__file__).resolve().parent.parent)
if _kg_to_script_root not in sys.path:
    sys.path.insert(0, _kg_to_script_root)
