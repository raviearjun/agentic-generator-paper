"""Layer 3 - TypeScript file generation for LangGraph."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader

from .models import LangGraphProject


def _create_jinja_env() -> Environment:
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    def _ts_escape(text: str) -> str:
        if not text:
            return ""
        # Escape literal newlines/carriage returns too: this text is embedded
        # in double-quoted string literals (not just backtick template
        # literals), which cannot contain a raw newline — and multi-paragraph
        # KG text (e.g. task descriptions) frequently has one, unlike the
        # short single-line agent prompts this filter originally only had to
        # handle.
        return (
            text.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("${", "\\${")
            .replace('"', '\\"')
            .replace("\r\n", "\\n")
            .replace("\n", "\\n")
            .replace("\r", "\\n")
        )

    env.filters["ts_escape"] = _ts_escape
    return env


def _to_pascal(name: str) -> str:
    chunks = [c for c in re.split(r"[^a-zA-Z0-9]+", name or "") if c]
    if not chunks:
        return "Graph"
    return "".join(c[:1].upper() + c[1:] for c in chunks)


def _collect_seed_fields(project: LangGraphProject) -> List[str]:
    """Collect distinct {placeholder} field names across all node task descriptions.

    Used to scaffold run.ts's `inputs` object so the user has a concrete list
    of fields to fill in (mirroring the source project's real input variables,
    e.g. CrewAI's inputs.yaml keys) instead of an empty, unusable object.
    """
    seen: List[str] = []
    seen_set = set()
    for node in project.nodes:
        for name in re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", node.task_description or ""):
            if name not in seen_set:
                seen_set.add(name)
                seen.append(name)
    return seen


def _build_common_context(project: LangGraphProject) -> Dict[str, Any]:
    node_by_iri = {n.iri: n for n in project.nodes}

    # Deduplicate nodes by their TypeScript name: two KG tasks can resolve to the
    # same ts_name, which would emit duplicate function/addNode declarations and
    # fail to compile ("symbol already declared"). Keep first occurrence.
    unique_nodes = []
    seen_node_names = set()
    for node in project.nodes:
        if node.ts_name in seen_node_names:
            continue
        seen_node_names.add(node.ts_name)
        unique_nodes.append(node)

    edges_named: List[Dict[str, str]] = []
    seen_edges = set()
    for edge in project.edges:
        src = node_by_iri.get(edge.source)
        tgt = node_by_iri.get(edge.target)
        if src and tgt:
            pair = (src.ts_name, tgt.ts_name)
            if pair in seen_edges:
                continue
            seen_edges.add(pair)
            edges_named.append({"source": src.ts_name, "target": tgt.ts_name})

    agent_by_iri = {a.iri: a for a in project.agents}

    return {
        "graph_name": project.name,
        "graph_class_name": _to_pascal(project.name),
        "agents": project.agents,
        "agent_by_iri": agent_by_iri,
        "tools": project.tools,
        "nodes": unique_nodes,
        "edges": edges_named,
        "routes": project.routes,
        "router_node_name": project.router_node_name,
        "start_node_name": project.start_node_name,
        "workflow_names": project.workflow_names,
        "seed_fields": _collect_seed_fields(project),
    }


def _build_manifest(output_dir: str, pattern: str) -> Dict[str, Any]:
    generated_files = []
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file == "manifest.json":
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, output_dir)
            generated_files.append(rel_path.replace("\\", "/"))

    return {
        "framework": "langgraph",
        "language": "typescript",
        "pattern": pattern,
        "generated_files": sorted(generated_files),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _write_base_files(output_dir: str, project: LangGraphProject) -> None:
    dependencies = {
        "@langchain/langgraph": "^0.2.0",
        "@langchain/core": "^0.3.0",
        "@langchain/openai": "^0.5.0",
        "zod": "^3.24.0",
    }
    # Add provider-specific packages actually imported by the generated code
    # (templates emit `ChatAnthropic` from '@langchain/anthropic' for anthropic
    # agents). Without this the import fails to resolve at runtime/typecheck.
    if any(agent.provider == "anthropic" for agent in project.agents):
        dependencies["@langchain/anthropic"] = "^0.3.0"

    package_json = {
        "name": "langgraph-generated-project",
        "version": "0.1.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "tsx run.ts",
            "typecheck": "tsc --noEmit",
        },
        "dependencies": dependencies,
        "devDependencies": {
            "typescript": "^5.6.0",
            "tsx": "^4.19.0",
            "@types/node": "^20.0.0",
        },
    }
    with open(os.path.join(output_dir, "package.json"), "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2)
        f.write("\n")

    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ESNext",
            "moduleResolution": "Bundler",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
        },
        "include": ["**/*.ts"],
    }
    with open(os.path.join(output_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
        json.dump(tsconfig, f, indent=2)
        f.write("\n")

    env_example = [
        "# Copy to .env and set actual values",
        "OPENAI_API_KEY=your_openai_api_key_here",
        "# Optional: OPENAI_BASE_URL=https://api.openai.com/v1",
    ]
    with open(os.path.join(output_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write("\n".join(env_example) + "\n")


def generate_project(project: LangGraphProject, output_dir: str) -> str:
    """Generate TypeScript LangGraph project from LangGraphProject IR."""
    os.makedirs(output_dir, exist_ok=True)
    nodes_dir = os.path.join(output_dir, "nodes")
    os.makedirs(nodes_dir, exist_ok=True)

    env = _create_jinja_env()
    ctx = _build_common_context(project)
    pattern = project.pattern_type

    if pattern == "linear":
        template = env.get_template("linear.index.ts.j2")
        content = template.render(**ctx)
        with open(os.path.join(output_dir, "index.ts"), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    elif pattern == "tool_calling":
        template = env.get_template("tool_calling.index.ts.j2")
        content = template.render(**ctx)
        with open(os.path.join(output_dir, "index.ts"), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    elif pattern == "branching":
        template = env.get_template("branching.index.ts.j2")
        content = template.render(**ctx)
        with open(os.path.join(output_dir, "index.ts"), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    else:
        # supervisor: full hub-and-spoke with explicit router node
        index_template = env.get_template("supervisor.index.ts.j2")
        types_template = env.get_template("supervisor.types.ts.j2")
        router_template = env.get_template("supervisor.router.ts.j2")
        general_template = env.get_template("supervisor.general-input.ts.j2")

        with open(os.path.join(output_dir, "index.ts"), "w", encoding="utf-8") as f:
            f.write(index_template.render(**ctx).strip() + "\n")

        with open(os.path.join(output_dir, "types.ts"), "w", encoding="utf-8") as f:
            f.write(types_template.render(**ctx).strip() + "\n")

        with open(os.path.join(nodes_dir, "router.ts"), "w", encoding="utf-8") as f:
            f.write(router_template.render(**ctx).strip() + "\n")

        with open(os.path.join(nodes_dir, "general-input.ts"), "w", encoding="utf-8") as f:
            f.write(general_template.render(**ctx).strip() + "\n")

    run_template = env.get_template("run.ts.j2")
    with open(os.path.join(output_dir, "run.ts"), "w", encoding="utf-8") as f:
        f.write(run_template.render(**ctx).strip() + "\n")

    _write_base_files(output_dir, project)

    manifest = _build_manifest(output_dir, pattern)
    with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"  [Generated] {output_dir}/ (TypeScript, pattern={pattern})")
    return output_dir
