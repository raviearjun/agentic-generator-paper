"""Dry run execution metrics for generated projects (Python and TypeScript)."""

from __future__ import annotations

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

from .node_runtime import ensure_node_modules

# Errors that indicate the generated code ran far enough to reach a real
# LLM/API call and was rejected only because of the dummy credentials.
_AUTH_SUCCESS_INDICATORS = [
    "AuthenticationError",
    "Incorrect API key",
    "invalid_api_key",
    "invalid x-api-key",
    "Could not resolve authentication method",
    "401",
    "unauthorized",
    "api_key",
    "APIKeyError",
    "APIConnectionError",
]

# (status, substrings-to-match) checked in order; first match wins.
_ERROR_TYPE_PATTERNS = [
    ("SYNTAX_ERROR", ["SyntaxError", "Transform failed", "Unexpected token"]),
    ("IMPORT_ERROR", [
        "ImportError", "ModuleNotFoundError",
        "Cannot find module", "ERR_MODULE_NOT_FOUND", "Cannot find package",
    ]),
    ("NAME_ERROR", ["NameError", "ReferenceError"]),
    ("TYPE_ERROR", ["TypeError"]),
    ("VALUE_ERROR", ["ValueError", "ZodError"]),
]


def dry_run_project(project_dir: Path, framework: str) -> dict:
    """Executes a dry-run check on a generated project using dummy credentials.

    Returns a dict with 'status' and 'output'.
    """
    framework = framework.lower()
    if framework in {"crewai", "autogen"}:
        main_py = project_dir / "main.py"
        if main_py.exists():
            return _run_and_classify(
                [sys.executable, str(main_py.resolve())],
                cwd=main_py.parent,
                env_overrides=_python_dummy_env(),
                timeout=10,
            )
    elif framework in {"langgraph", "mastra"}:
        entry = _find_ts_entry(project_dir)
        if entry is not None:
            ok, install_err = ensure_node_modules(project_dir)
            if not ok:
                return {"status": "DEPENDENCY_ERROR", "output": install_err[-1000:]}
            tsx_bin = project_dir.resolve() / "node_modules" / ".bin" / "tsx"
            cmd = [str(tsx_bin), str(entry.resolve())]
            return _run_and_classify(
                cmd,
                cwd=project_dir,
                env_overrides=_typescript_dummy_env(),
                timeout=20,
            )
    return {"status": "N/A", "output": ""}


def _python_dummy_env() -> dict:
    return {"OPENAI_API_KEY": "sk-dummy"}


def _typescript_dummy_env() -> dict:
    return {
        "OPENAI_API_KEY": "sk-dummy",
        "ANTHROPIC_API_KEY": "sk-ant-dummy",
        "DATABASE_URL": "file:local.db",
        "POSTGRES_URL": "postgres://dummy:dummy@localhost:5432/dummy",
        "MONGODB_URI": "mongodb://localhost:27017/dummy",
        "MONGODB_DB_NAME": "dummy",
    }


def _find_ts_entry(project_dir: Path) -> Optional[Path]:
    """Resolves the runnable entry point of a TS project from package.json, falling back to index.ts."""
    package_json = project_dir / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            main = data.get("main")
            if main:
                candidate = project_dir / main
                if candidate.exists():
                    return candidate
        except Exception:
            pass
    fallback = project_dir / "index.ts"
    return fallback if fallback.exists() else None


def _run_and_classify(cmd: list[str], cwd: Path, env_overrides: dict, timeout: int) -> dict:
    """Runs cmd with dummy credentials and classifies the outcome.

    A run is treated as SUCCESS_DUMMY if it exits cleanly, or if it fails only
    because the dummy credentials were rejected by a real API call (proving the
    generated code imports and wires up correctly up to that point).
    """
    env = os.environ.copy()
    env.update(env_overrides)
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd.resolve()),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        error_msg = res.stderr.strip() or res.stdout.strip()

        is_success = res.returncode == 0 or any(
            ind in error_msg for ind in _AUTH_SUCCESS_INDICATORS
        )
        if is_success:
            return {"status": "SUCCESS_DUMMY", "output": ""}

        error_type = "OTHER_ERROR"
        for status, needles in _ERROR_TYPE_PATTERNS:
            if any(needle in error_msg for needle in needles):
                error_type = status
                break

        details = "\n".join(error_msg.splitlines()[-5:])
        return {"status": error_type, "output": details}

    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "output": f"Proyek timeout setelah {timeout} detik"}
    except Exception as exc:
        return {"status": "OTHER_ERROR", "output": str(exc)}
