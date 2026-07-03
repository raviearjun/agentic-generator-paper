"""Shared helpers for running Node/TypeScript generated projects (LangGraph, Mastra)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Tuple


def _missing_dependencies(project_dir: Path) -> bool:
    """Return True if package.json declares a dependency not present in node_modules.

    Catches the case where a project was installed by a previous run but the
    generator has since added a new dependency (e.g. @langchain/anthropic) that
    the stale node_modules doesn't contain.
    """
    package_json = project_dir / "package.json"
    if not package_json.exists():
        return False
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except Exception:
        return False
    node_modules = project_dir / "node_modules"
    deps = {}
    deps.update(data.get("dependencies", {}) or {})
    deps.update(data.get("devDependencies", {}) or {})
    for name in deps:
        # Scoped packages (@scope/name) resolve to node_modules/@scope/name.
        if not (node_modules / Path(name)).exists():
            return True
    return False


def ensure_node_modules(project_dir: Path, timeout: int = 180) -> Tuple[bool, str]:
    """Ensures npm dependencies are installed for a TS project, installing them on demand.

    Runs `npm install` if node_modules is absent or if any declared dependency is
    missing (e.g. after the generator added a new one); otherwise a cheap no-op.
    Returns (ok, error_output).
    """
    if not (project_dir / "package.json").exists():
        return False, "package.json not found"
    if (project_dir / "node_modules").exists() and not _missing_dependencies(project_dir):
        return True, ""
    try:
        res = subprocess.run(
            ["npm", "install", "--no-audit", "--no-fund"],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if res.returncode != 0:
            return False, (res.stderr.strip() or res.stdout.strip())
        return True, ""
    except subprocess.TimeoutExpired:
        return False, f"npm install timed out after {timeout}s"
    except Exception as exc:
        return False, str(exc)
