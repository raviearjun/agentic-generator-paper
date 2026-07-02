"""CLI for OEC/WGI evaluation of KG-to-framework generated outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List

from .config import framework_configs
from .extractors.code_extractor import extract_code
from .extractors.kg_extractor import extract_kg
from .metrics.oec import calculate_oec
from .metrics.wgi import calculate_wgi
from .metrics.compilation import compile_project
from .metrics.dry_run import dry_run_project
from .pairing import pair_projects
from .reports.markdown_report import render_markdown


def main() -> None:
    args = _parse_args()
    root = args.root.resolve()
    configs = framework_configs(root)

    selected = [args.framework] if args.framework != "all" else list(configs.keys())
    base_output_dir = args.output_dir.resolve()
    
    all_framework_results = []

    for key in selected:
        config = configs[key]
        framework_result = _evaluate_framework(key, config)
        all_framework_results.append(framework_result)
        
        framework_output_dir = base_output_dir / key
        framework_output_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = framework_output_dir / "oec_wgi_results.json"
        md_path = framework_output_dir / "oec_wgi_results.md"
        
        results = {"root": str(root), "frameworks": [framework_result]}
        json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        md_path.write_text(render_markdown(results), encoding="utf-8")

        print(f"Evaluation for {config.name} written to {json_path}")
        print(f"Report for {config.name} written to {md_path}")

    if args.framework == "all":
        base_output_dir.mkdir(parents=True, exist_ok=True)
        json_path = base_output_dir / "oec_wgi_results.json"
        md_path = base_output_dir / "oec_wgi_results.md"
        
        combined_results = {"root": str(root), "frameworks": all_framework_results}
        json_path.write_text(json.dumps(combined_results, indent=2), encoding="utf-8")
        md_path.write_text(render_markdown(combined_results), encoding="utf-8")

        print(f"Combined evaluation written to {json_path}")
        print(f"Combined report written to {md_path}")


def _evaluate_framework(key: str, config) -> Dict[str, object]:
    projects = []
    for kg_path, project_dir, project_name in pair_projects(config):
        print(f"[{config.name}] {project_name}")
        if not project_dir.exists():
            projects.append(
                {
                    "project": project_name,
                    "kg_path": str(kg_path),
                    "output_dir": str(project_dir),
                    "status": "missing_output",
                    "error": f"Generated output directory not found: {project_dir}",
                }
            )
            continue
        try:
            kg = extract_kg(kg_path)
            code = extract_code(project_dir, key)
            oec = calculate_oec(kg, code)
            wgi = calculate_wgi(kg, code)

            # 1. Compilation check
            syntax_ok = compile_project(project_dir, key)

            # 2. Dry run execution check
            run_res = dry_run_project(project_dir, key)
            run_status = run_res["status"]
            run_output = run_res["output"]

            projects.append(
                {
                    "project": project_name,
                    "kg_path": str(kg_path),
                    "output_dir": str(project_dir),
                    "status": "ok",
                    "kg_element_count": len(kg.elements),
                    "code_element_count": len(code.elements),
                    "oec": oec,
                    "wgi": wgi,
                    "syntax_ok": syntax_ok,
                    "run_status": run_status,
                    "run_output": run_output,
                }
            )
        except Exception as exc:
            projects.append(
                {
                    "project": project_name,
                    "kg_path": str(kg_path),
                    "output_dir": str(project_dir),
                    "status": "error",
                    "error": str(exc),
                }
            )

    return {
        "key": key,
        "name": config.name,
        "kg_dir": str(config.kg_dir),
        "output_dir": str(config.output_dir),
        "summary": _summary(projects),
        "projects": projects,
    }


def _summary(projects: List[Dict[str, object]]) -> Dict[str, object]:
    ok_projects = [project for project in projects if project.get("status") == "ok"]
    errors = len(projects) - len(ok_projects)

    return {
        "projects": len(projects),
        "evaluated": len(ok_projects),
        "errors": errors,
        "avg_oec_all": _avg(project["oec"]["all_extracted"]["score"] for project in ok_projects),
        "avg_oec_important": _avg(project["oec"]["important_subset"]["score"] for project in ok_projects),
        "avg_wgi": _avg(project["wgi"]["score"] for project in ok_projects),
        "avg_edge_f1": _avg(project["wgi"]["edge_f1"] for project in ok_projects),
        "syntax_success_rate": _avg(1.0 if project.get("syntax_ok") else 0.0 for project in ok_projects),
        "run_success_rate": _avg(
            1.0 if project.get("run_status") == "SUCCESS_DUMMY" or (project.get("run_status") == "N/A" and project.get("syntax_ok")) else 0.0
            for project in ok_projects
        ),
    }


def _avg(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate KG-to-framework conversion with OEC and WGI.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (unused; kg/output dirs are resolved relative to kg_to_script/).",
    )
    parser.add_argument(
        "--framework",
        choices=["all", "crewai", "autogen", "langgraph", "mastra"],
        default="all",
        help="Framework to evaluate.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evaluation_reports"),
        help="Directory for JSON and Markdown evaluation reports.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
