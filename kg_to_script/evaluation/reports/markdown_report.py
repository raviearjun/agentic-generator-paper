"""Markdown report rendering for OEC/WGI evaluation."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List


def render_markdown(results: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# OEC/WGI Evaluation Report")
    lines.append("")
    
    now = datetime.now()
    lines.append(f"- **Date:** {now.strftime('%Y-%m-%d')}")
    lines.append(f"- **Time:** {now.strftime('%H:%M:%S')} (Local Time)")
    if "root" in results:
        lines.append(f"- **Workspace Root:** `{results['root']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Framework | Projects | Errors | CCR | WGI | Edge F1 | SCR | ER |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for framework in results.get("frameworks", []):
        summary = framework.get("summary", {})
        lines.append(
            "| {name} | {projects} | {errors} | {ccr} | {wgi} | {edge_f1} | {scr} | {er} |".format(
                name=framework.get("name", ""),
                projects=summary.get("projects", 0),
                errors=summary.get("errors", 0),
                ccr=_pct(summary.get("concept_coverage_rate")),
                wgi=_pct(summary.get("avg_wgi")),
                edge_f1=_pct(summary.get("avg_edge_f1")),
                scr=_pct(summary.get("syntactic_correctness_rate")),
                er=_pct(summary.get("executability_rate")),
            )
        )

    lines.append("")
    lines.append("## Project Details")
    for framework in results.get("frameworks", []):
        lines.append("")
        lines.append(f"### {framework.get('name', '')}")
        lines.append("")
        lines.append("| Project | Status | CCR | Missing Important | WGI | Missing Edges | Extra Edges | SCR | Run Status |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
        for project in framework.get("projects", []):
            if project.get("status") != "ok":
                lines.append(
                    f"| `{project.get('project', '')}` | error | - | - | - | - | - | - | - | - |"
                )
                continue
            oec = project["oec"]
            wgi = project["wgi"]
            scr_str = "✅ OK" if project.get("syntax_ok") else "❌ FAIL"
            run_status = project.get("run_status", "N/A")
            run_str = "✅ SUCCESS_DUMMY" if run_status == "SUCCESS_DUMMY" else (f"❌ {run_status}" if run_status != "N/A" else "➖ N/A")
            lines.append(
                "| `{project}` | ok | {ccr} | {missing_important} | {wgi} | {missing_edges} | {extra_edges} | {scr} | {run} |".format(
                    project=project.get("project", ""),
                    ccr=_pct(oec["important_subset"]["score"]),
                    missing_important=len(oec["important_subset"].get("missing", [])),
                    wgi=_pct(wgi["score"]),
                    missing_edges=len(wgi.get("missing_edges", [])),
                    extra_edges=len(wgi.get("extra_edges", [])),
                    scr=scr_str,
                    run=run_str,
                )
            )

        failures = [p for p in framework.get("projects", []) if p.get("status") == "ok" and p.get("run_status") not in ("SUCCESS_DUMMY", "N/A")]
        if failures:
            lines.append("")
            lines.append(f"#### Dry-Run Execution Failures ({framework.get('name', '')})")
            lines.append("")
            for p in failures:
                lines.append(f"- **{p['project']}** (`{p['run_status']}`):")
                lines.append("  ```")
                for line in str(p.get("run_output", "")).splitlines():
                    lines.append(f"  {line}")
                lines.append("  ```")

        errors = [project for project in framework.get("projects", []) if project.get("status") != "ok"]
        if errors:
            lines.append("")
            lines.append("#### Errors")
            lines.append("")
            for project in errors:
                lines.append(f"- `{project.get('project', '')}`: {project.get('error', '')}")

    lines.append("")
    lines.append("## Lowest CCR (Concept Coverage Rate)")
    lines.append("")
    for project in _lowest_projects(results, "important"):
        lines.append(
            f"- `{project['framework']}/{project['project']}`: {_pct(project['score'])} ({project['missing']} missing important elements)"
        )

    lines.append("")
    lines.append("## Lowest WGI")
    lines.append("")
    for project in _lowest_projects(results, "wgi"):
        lines.append(
            f"- `{project['framework']}/{project['project']}`: {_pct(project['score'])} ({project['missing_edges']} missing edges, {project['extra_edges']} extra edges)"
        )

    lines.append("")
    return "\n".join(lines)


def _pct(value: object) -> str:
    if value is None:
        return "-"
    return f"{float(value) * 100:.1f}%"


def _lowest_projects(results: Dict[str, object], metric: str) -> List[Dict[str, object]]:
    rows = []
    for framework in results.get("frameworks", []):
        for project in framework.get("projects", []):
            if project.get("status") != "ok":
                continue
            if metric == "important":
                score = project["oec"]["important_subset"]["score"]
                rows.append(
                    {
                        "framework": framework.get("name", ""),
                        "project": project.get("project", ""),
                        "score": score,
                        "missing": len(project["oec"]["important_subset"].get("missing", [])),
                    }
                )
            else:
                rows.append(
                    {
                        "framework": framework.get("name", ""),
                        "project": project.get("project", ""),
                        "score": project["wgi"]["score"],
                        "missing_edges": len(project["wgi"].get("missing_edges", [])),
                        "extra_edges": len(project["wgi"].get("extra_edges", [])),
                    }
                )
    return sorted(rows, key=lambda row: row["score"])[:10]
