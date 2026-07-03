"""Markdown report rendering for cross-framework interoperability evaluation."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


# Framework display names keyed by internal key.
_DISPLAY_NAMES = {
    "crewai": "CrewAI",
    "autogen": "AutoGen",
    "langgraph": "LangGraph",
    "mastra": "Mastra",
}

FRAMEWORK_KEYS = ["crewai", "autogen", "langgraph", "mastra"]


def render_interop_markdown(results: Dict[str, Any]) -> str:
    """Render a full interop evaluation report as Markdown."""
    lines: List[str] = []

    lines.append("# Cross-Framework Interoperability Evaluation Report")
    lines.append("")
    lines.append(f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Local Time)")
    if "root" in results:
        lines.append(f"- **Workspace Root:** `{results['root']}`")
    lines.append("")

    matrix = results.get("matrix", {})
    pairs = results.get("pairs", [])
    frameworks = results.get("frameworks", FRAMEWORK_KEYS)

    # ── 1. CFCS Compatibility Matrix ──
    _render_matrix_table(lines, matrix, frameworks, "cfcs", "CFCS (Cross-Framework Compatibility Score)")
    lines.append("")
    lines.append("> CFCS = 0.2·SCR + 0.2·ER + 0.3·CCR + 0.3·WGI  ")
    lines.append("> SCR = Syntactic Correctness Rate, ER = Executability Rate, CCR = Concept Coverage Rate")
    lines.append("> (When ER is N/A for TypeScript targets, SCR weight is doubled to 0.4)")
    lines.append("")

    # ── 2. Individual metric matrices ──
    _render_matrix_table(lines, matrix, frameworks, "syntactic_correctness_rate", "SCR (Syntactic Correctness Rate)")
    lines.append("")
    _render_matrix_table(lines, matrix, frameworks, "concept_coverage_rate", "CCR (Concept Coverage Rate)")
    lines.append("")
    _render_matrix_table(lines, matrix, frameworks, "avg_wgi", "WGI (Workflow Graph Isomorphism)")
    lines.append("")
    _render_matrix_table(lines, matrix, frameworks, "oec_all", "OEC All (Full Ontology Element Coverage)")
    lines.append("")

    # ── 3. Generation Success Matrix ──
    lines.append("## Generation Success Matrix")
    lines.append("")
    header = "| Source ↓ \\ Target → | " + " | ".join(_DISPLAY_NAMES.get(f, f) for f in frameworks) + " |"
    sep = "| :--- | " + " | ".join(":---:" for _ in frameworks) + " |"
    lines.append(header)
    lines.append(sep)
    for src in frameworks:
        row_cells = []
        for tgt in frameworks:
            cell = matrix.get(src, {}).get(tgt, {})
            total = cell.get("total_kgs", 0)
            gen_ok = cell.get("generated_ok", 0)
            gen_err = cell.get("generation_errors", 0)
            row_cells.append(f"{gen_ok}/{total} ({gen_err} err)")
        lines.append(f"| **{_DISPLAY_NAMES.get(src, src)}** | " + " | ".join(row_cells) + " |")
    lines.append("")

    # ── 4. Per-pair detailed sections ──
    lines.append("## Pair Details")
    lines.append("")

    for pair in pairs:
        src = pair["source"]
        tgt = pair["target"]
        is_same = pair.get("is_same_framework", False)
        tag = " _(same-framework baseline)_" if is_same else ""
        lines.append(f"### {_DISPLAY_NAMES.get(src, src)} → {_DISPLAY_NAMES.get(tgt, tgt)}{tag}")
        lines.append("")

        summary = pair.get("summary", {})
        if not summary:
            lines.append("_No KGs found or KG directory missing._")
            lines.append("")
            continue

        # Summary table
        lines.append("| Metric | Value |")
        lines.append("| :--- | :--- |")
        lines.append(f"| Total KGs | {summary.get('total_kgs', 0)} |")
        lines.append(f"| Generated OK | {summary.get('generated_ok', 0)} |")
        lines.append(f"| Evaluated OK | {summary.get('evaluated_ok', 0)} |")
        lines.append(f"| Generation Errors | {summary.get('generation_errors', 0)} |")
        lines.append(f"| SCR (Syntactic Correctness Rate) | {_pct(summary.get('syntactic_correctness_rate'))} |")
        er_val = summary.get("executability_rate")
        er_na = summary.get("executability_rate_na", True)
        lines.append(f"| ER (Executability Rate) | {_pct(er_val) if not er_na else 'N/A (TypeScript target)'} |")
        lines.append(f"| OEC All | {_pct(summary.get('oec_all'))} |")
        lines.append(f"| CCR (Concept Coverage Rate) | {_pct(summary.get('concept_coverage_rate'))} |")
        lines.append(f"| WGI | {_pct(summary.get('avg_wgi'))} |")
        lines.append(f"| Edge F1 | {_pct(summary.get('avg_edge_f1'))} |")
        lines.append(f"| **CFCS** | **{_pct(summary.get('cfcs'))}** |")
        lines.append("")

        # Project details table
        projects = pair.get("projects", [])
        if projects:
            lines.append("<details>")
            lines.append(f"<summary>Project details ({len(projects)} KGs)</summary>")
            lines.append("")
            lines.append("| Project | Status | SCR | ER | CCR | WGI |")
            lines.append("| :--- | :---: | :---: | :---: | :---: | :---: |")
            for p in projects:
                status = p.get("status", "?")
                if status == "ok":
                    scr_str = "✅" if p.get("syntax_ok") else "❌"
                    run_str = _run_emoji(p.get("run_status"))
                    ccr = _pct(p.get("oec", {}).get("important_subset", {}).get("score"))
                    wgi_val = _pct(p.get("wgi", {}).get("score"))
                    lines.append(f"| `{p['project']}` | ✅ ok | {scr_str} | {run_str} | {ccr} | {wgi_val} |")
                else:
                    err_brief = (p.get("error", "")[:60] + "…") if len(p.get("error", "")) > 60 else p.get("error", "")
                    lines.append(f"| `{p['project']}` | ❌ {status} | - | - | - | - |")
            lines.append("")
            lines.append("</details>")
            lines.append("")

        # Generation errors detail
        gen_errors = [p for p in projects if p.get("status") == "generation_error"]
        if gen_errors:
            lines.append(f"<details>")
            lines.append(f"<summary>⚠️ Generation errors ({len(gen_errors)})</summary>")
            lines.append("")
            for p in gen_errors:
                lines.append(f"- **{p['project']}**: `{p.get('error', '')}`")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    # ── 5. Overall aggregate ──
    lines.append("## Overall Interoperability Summary")
    lines.append("")

    cross_pairs = [p for p in pairs if not p.get("is_same_framework")]
    same_pairs = [p for p in pairs if p.get("is_same_framework")]

    if cross_pairs:
        cross_summaries = [p["summary"] for p in cross_pairs if p.get("summary")]
        if cross_summaries:
            avg_cfcs = _avg_field(cross_summaries, "cfcs")
            avg_scr = _avg_field(cross_summaries, "syntactic_correctness_rate")
            avg_ccr = _avg_field(cross_summaries, "concept_coverage_rate")
            avg_wgi = _avg_field(cross_summaries, "avg_wgi")

            lines.append("### Cross-Framework (excluding same-framework)")
            lines.append("")
            lines.append(f"- **Avg CFCS:** {_pct(avg_cfcs)}")
            lines.append(f"- **Avg SCR (Syntactic Correctness Rate):** {_pct(avg_scr)}")
            lines.append(f"- **Avg CCR (Concept Coverage Rate):** {_pct(avg_ccr)}")
            lines.append(f"- **Avg WGI:** {_pct(avg_wgi)}")
            lines.append(f"- **Cross-framework pairs evaluated:** {len(cross_summaries)}")
            lines.append("")

    if same_pairs:
        same_summaries = [p["summary"] for p in same_pairs if p.get("summary")]
        if same_summaries:
            avg_cfcs = _avg_field(same_summaries, "cfcs")
            lines.append("### Same-Framework Baselines")
            lines.append("")
            lines.append(f"- **Avg CFCS (baseline):** {_pct(avg_cfcs)}")
            lines.append("")

    lines.append("")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _render_matrix_table(
    lines: List[str],
    matrix: Dict[str, Dict[str, Dict[str, Any]]],
    frameworks: List[str],
    metric_key: str,
    title: str,
) -> None:
    """Append a 4×4 matrix table for a given metric."""
    lines.append(f"## {title}")
    lines.append("")
    header = "| Source ↓ \\ Target → | " + " | ".join(_DISPLAY_NAMES.get(f, f) for f in frameworks) + " |"
    sep = "| :--- | " + " | ".join(":---:" for _ in frameworks) + " |"
    lines.append(header)
    lines.append(sep)
    for src in frameworks:
        cells = []
        for tgt in frameworks:
            val = matrix.get(src, {}).get(tgt, {}).get(metric_key)
            if val is not None:
                cells.append(_pct(val))
            else:
                cells.append("-")
        lines.append(f"| **{_DISPLAY_NAMES.get(src, src)}** | " + " | ".join(cells) + " |")


def _pct(value: Optional[float]) -> str:
    if value is None:
        return "-"
    return f"{float(value) * 100:.1f}%"


def _run_emoji(status: Optional[str]) -> str:
    if status == "SUCCESS_DUMMY":
        return "✅"
    if status in (None, "N/A"):
        return "➖"
    return f"❌ {status}"


def _avg_field(summaries: List[Dict[str, Any]], field: str) -> float:
    vals = [s[field] for s in summaries if field in s and s[field] is not None]
    return sum(vals) / len(vals) if vals else 0.0
