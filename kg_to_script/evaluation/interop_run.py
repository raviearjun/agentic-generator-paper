"""Cross-framework interoperability evaluation.

Tests whether KGs from one framework can be successfully translated into
runnable code for a different target framework, and measures the fidelity
of that translation using OEC, WGI, and runtime metrics.

Usage:
    python -m src.evaluation.interop_run
    python -m src.evaluation.interop_run --source crewai --target autogen
    python -m src.evaluation.interop_run --source crewai  # all targets
"""

from __future__ import annotations

import argparse
import json
import shutil
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.core.extractor import extract_project

from .config import FrameworkConfig, framework_configs
from .extractors.code_extractor import extract_code
from .extractors.kg_extractor import extract_kg
from .metrics.compilation import compile_project
from .metrics.dry_run import dry_run_project
from .metrics.oec import calculate_oec
from .metrics.wgi import calculate_wgi
from .pairing import project_name_from_kg
from .reports.interop_report import render_interop_markdown

# Framework keys in canonical order.
FRAMEWORK_KEYS = ["crewai", "autogen", "langgraph", "mastra"]

# CFCS default weights.
_W_SCR = 0.2
_W_ER = 0.2
_W_OEC = 0.3
_W_WGI = 0.3


# ──────────────────────────────────────────────
# Adapter / generator registry
# ──────────────────────────────────────────────

def _get_adapter_and_generator(target_key: str):
    """Lazy-import the adapter and generator for the given target framework.

    Returns:
        (adapt_fn, generate_fn)
    """
    if target_key == "crewai":
        from src.frameworks.crewai.adapter import adapt
        from src.frameworks.crewai.generator import generate_project as gen
        return adapt, gen
    if target_key == "autogen":
        from src.frameworks.autogen.adapter import adapt
        from src.frameworks.autogen.generator import generate_project as gen
        return adapt, gen
    if target_key == "langgraph":
        from src.frameworks.langgraph.adapter import adapt
        from src.frameworks.langgraph.generator import generate_project as gen
        return adapt, gen
    if target_key == "mastra":
        from src.frameworks.mastra.adapter import adapt
        from src.frameworks.mastra.generator import generate_project as gen
        return adapt, gen
    raise ValueError(f"Unknown target framework: {target_key}")


def _target_ext(target_key: str) -> str:
    """Return the file extension for generated code of the target framework."""
    return ".ts" if target_key in {"langgraph", "mastra"} else ".py"


# ──────────────────────────────────────────────
# Core translation & evaluation
# ──────────────────────────────────────────────

def _translate_and_evaluate(
    kg_path: Path,
    project_name: str,
    source_key: str,
    target_key: str,
    output_dir: Path,
) -> Dict[str, Any]:
    """Translate a single KG from source → target and evaluate.

    Steps:
        1. Extract canonical IR (AgenticProject) from the KG.
        2. Run the target framework's adapter + generator.
        3. Evaluate: compilation, dry-run, OEC, WGI.
    """
    result: Dict[str, Any] = {
        "project": project_name,
        "kg_path": str(kg_path),
        "source": source_key,
        "target": target_key,
        "output_dir": str(output_dir),
    }

    # Step 1: extract canonical IR
    try:
        canonical_project = extract_project(str(kg_path))
    except Exception as exc:
        result["status"] = "extraction_error"
        result["error"] = str(exc)
        return result

    # Step 2: adapt + generate for target framework
    try:
        adapt_fn, gen_fn = _get_adapter_and_generator(target_key)
        target_project = adapt_fn(canonical_project)

        # For mastra: override project_var_name to prevent overwrites
        if target_key == "mastra" and hasattr(target_project, "project_var_name"):
            target_project.project_var_name = project_name

        # Some generators (e.g. mastra) nest the actual project one directory
        # deeper than output_dir and return that path; others write flat into
        # output_dir and return it unchanged. Always use the returned path for
        # downstream evaluation so compilation/dry-run look in the right place.
        generated_dir = Path(gen_fn(target_project, str(output_dir)))
        result["output_dir"] = str(generated_dir)
    except Exception as exc:
        result["status"] = "generation_error"
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["traceback"] = traceback.format_exc()
        return result

    # Step 3: evaluate the generated output
    try:
        kg_eval = extract_kg(kg_path)
        code_eval = extract_code(generated_dir, target_key)

        oec = calculate_oec(kg_eval, code_eval)
        wgi = calculate_wgi(kg_eval, code_eval)
        syntax_ok = compile_project(generated_dir, target_key)
        run_res = dry_run_project(generated_dir, target_key)

        result["status"] = "ok"
        result["oec"] = oec
        result["wgi"] = wgi
        result["syntax_ok"] = syntax_ok
        result["run_status"] = run_res["status"]
        result["run_output"] = run_res["output"]
    except Exception as exc:
        result["status"] = "evaluation_error"
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


# ──────────────────────────────────────────────
# Cross-framework pair evaluation
# ──────────────────────────────────────────────

def _evaluate_pair(
    source_key: str,
    target_key: str,
    source_config: FrameworkConfig,
    interop_base: Path,
) -> Dict[str, Any]:
    """Evaluate all KGs from source_key translated to target_key."""
    pair_output_base = interop_base / source_key / target_key
    pair_output_base.mkdir(parents=True, exist_ok=True)

    kg_dir = source_config.kg_dir
    if not kg_dir.exists():
        return {
            "source": source_key,
            "target": target_key,
            "status": "missing_kg_dir",
            "error": f"KG directory not found: {kg_dir}",
            "projects": [],
            "summary": {},
        }

    kg_files = sorted(kg_dir.glob(source_config.kg_glob))
    projects: List[Dict[str, Any]] = []

    for kg_path in kg_files:
        project_name = project_name_from_kg(kg_path)
        output_dir = pair_output_base / project_name

        label = f"[{source_key} → {target_key}] {project_name}"
        print(f"  {label}")

        result = _translate_and_evaluate(
            kg_path=kg_path,
            project_name=project_name,
            source_key=source_key,
            target_key=target_key,
            output_dir=output_dir,
        )
        projects.append(result)

    summary = _pair_summary(projects)
    return {
        "source": source_key,
        "target": target_key,
        "status": "ok",
        "projects": projects,
        "summary": summary,
    }


def _pair_summary(projects: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute aggregate metrics for a source→target pair."""
    total = len(projects)
    if total == 0:
        return {}

    ok = [p for p in projects if p.get("status") == "ok"]
    gen_errors = [p for p in projects if p.get("status") == "generation_error"]
    eval_errors = [p for p in projects if p.get("status") == "evaluation_error"]
    extract_errors = [p for p in projects if p.get("status") == "extraction_error"]

    # SCR: syntactic correctness rate among successfully generated projects
    generated = [p for p in projects if p.get("status") in ("ok", "evaluation_error")]
    syntax_ok_count = sum(1 for p in ok if p.get("syntax_ok"))
    syntactic_correctness_rate = syntax_ok_count / len(generated) if generated else 0.0

    # ER: executability rate (dry-run success rate)
    executability_eligible = [
        p for p in ok
        if p.get("run_status") not in (None, "N/A")
    ]
    executability_success = sum(
        1 for p in ok
        if p.get("run_status") == "SUCCESS_DUMMY"
    )
    executability_rate_na = all(p.get("run_status") in (None, "N/A") for p in ok) if ok else True
    executability_rate = (
        executability_success / len(executability_eligible)
        if executability_eligible
        else (1.0 if executability_rate_na else 0.0)
    )

    # OEC averages
    oec_all = _avg([p["oec"]["all_extracted"]["score"] for p in ok])
    concept_coverage_rate = _avg([p["oec"]["important_subset"]["score"] for p in ok])

    # WGI average
    avg_wgi = _avg([p["wgi"]["score"] for p in ok])
    avg_edge_f1 = _avg([p["wgi"]["edge_f1"] for p in ok])

    # CFCS: composite score
    if executability_rate_na:
        # No dry-run data — redistribute ER weight
        cfcs = (_W_SCR + _W_ER) * syntactic_correctness_rate + _W_OEC * concept_coverage_rate + _W_WGI * avg_wgi
    else:
        cfcs = (
            _W_SCR * syntactic_correctness_rate
            + _W_ER * executability_rate
            + _W_OEC * concept_coverage_rate
            + _W_WGI * avg_wgi
        )

    return {
        "total_kgs": total,
        "generated_ok": len(ok) + len(eval_errors),
        "evaluated_ok": len(ok),
        "generation_errors": len(gen_errors),
        "extraction_errors": len(extract_errors),
        "evaluation_errors": len(eval_errors),
        "syntactic_correctness_rate": syntactic_correctness_rate,
        "executability_rate": executability_rate,
        "executability_rate_na": executability_rate_na,
        "oec_all": oec_all,
        "concept_coverage_rate": concept_coverage_rate,
        "avg_wgi": avg_wgi,
        "avg_edge_f1": avg_edge_f1,
        "cfcs": cfcs,
    }


def _avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


# ──────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────

def main() -> None:
    args = _parse_args()
    root = args.root.resolve()
    configs = framework_configs(root)

    sources = [args.source] if args.source != "all" else FRAMEWORK_KEYS
    targets = [args.target] if args.target != "all" else FRAMEWORK_KEYS

    interop_base = root / "generated_projects" / "output_interop"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean previous interop outputs if requested
    if args.clean and interop_base.exists():
        print(f"Cleaning previous interop outputs: {interop_base}")
        shutil.rmtree(interop_base)

    all_pairs: List[Dict[str, Any]] = []

    for source_key in sources:
        for target_key in targets:
            is_same = source_key == target_key
            label = f"{source_key} → {target_key}" + (" (same-framework)" if is_same else "")
            print(f"\n{'=' * 60}")
            print(f"  Interop: {label}")
            print(f"{'=' * 60}")

            pair_result = _evaluate_pair(
                source_key=source_key,
                target_key=target_key,
                source_config=configs[source_key],
                interop_base=interop_base,
            )
            pair_result["is_same_framework"] = is_same
            all_pairs.append(pair_result)

            summary = pair_result.get("summary", {})
            if summary:
                print(f"  SCR={_pct(summary.get('syntactic_correctness_rate'))} "
                      f"ER={_pct(summary.get('executability_rate'))} "
                      f"CCR={_pct(summary.get('concept_coverage_rate'))} "
                      f"WGI={_pct(summary.get('avg_wgi'))} "
                      f"CFCS={_pct(summary.get('cfcs'))}")

    # Build full results payload
    results = {
        "root": str(root),
        "timestamp": datetime.now().isoformat(),
        "frameworks": FRAMEWORK_KEYS,
        "pairs": all_pairs,
        "matrix": _build_matrix(all_pairs),
    }

    # Write reports
    json_path = output_dir / "interop_results.json"
    md_path = output_dir / "interop_results.md"

    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    md_path.write_text(render_interop_markdown(results), encoding="utf-8")

    print(f"\nInterop JSON: {json_path}")
    print(f"Interop Report: {md_path}")


def _build_matrix(pairs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Build a nested dict: matrix[source][target] = summary metrics."""
    matrix: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for pair in pairs:
        src = pair["source"]
        tgt = pair["target"]
        summary = pair.get("summary", {})
        if src not in matrix:
            matrix[src] = {}
        matrix[src][tgt] = {
            "cfcs": summary.get("cfcs", 0.0),
            "syntactic_correctness_rate": summary.get("syntactic_correctness_rate", 0.0),
            "executability_rate": summary.get("executability_rate", 0.0),
            "executability_rate_na": summary.get("executability_rate_na", True),
            "oec_all": summary.get("oec_all", 0.0),
            "concept_coverage_rate": summary.get("concept_coverage_rate", 0.0),
            "avg_wgi": summary.get("avg_wgi", 0.0),
            "avg_edge_f1": summary.get("avg_edge_f1", 0.0),
            "total_kgs": summary.get("total_kgs", 0),
            "generated_ok": summary.get("generated_ok", 0),
            "generation_errors": summary.get("generation_errors", 0),
        }
    return matrix


def _pct(value: Optional[float]) -> str:
    if value is None:
        return "-"
    return f"{value * 100:.1f}%"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-framework interoperability evaluation."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (used as base for interop output artifacts).",
    )
    parser.add_argument(
        "--source",
        choices=["all"] + FRAMEWORK_KEYS,
        default="all",
        help="Source framework whose KGs to translate.",
    )
    parser.add_argument(
        "--target",
        choices=["all"] + FRAMEWORK_KEYS,
        default="all",
        help="Target framework to generate code for.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent.parent / "evaluation_reports",
        help="Directory for JSON and Markdown interop reports.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove previous interop output before running.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
