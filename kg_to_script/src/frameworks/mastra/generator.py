"""
Layer 3 – TypeScript File Generation for Mastra AI

Generates a complete Mastra AI TypeScript project from a MastraProject IR:
  - src/mastra/index.ts       (Mastra instance + agent/workflow registration)
  - src/mastra/agents/*.ts    (Agent definitions)
  - src/mastra/tools/*.ts     (Tool definitions with createTool)
  - src/mastra/workflows/*.ts (Workflow + step definitions) - Milestone 2+
  - src/mastra/memory/*.ts    (Memory instances with storage backend) - Milestone 3+
  - package.json              (npm dependencies)
  - tsconfig.json             (TypeScript configuration)
  - .env.example              (Environment variables)
  - README.md                 (Project documentation)

Design decisions:
  - All TypeScript files use Jinja2 templates
  - Auto-infer dependencies from agents, tools, models, and memory backends
  - Generate TODO comments for custom tool implementations
  - Storage tools (MongoDBStore, PgVector, etc.) are skipped in createTool() generation
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Set

from jinja2 import Environment, FileSystemLoader

from .models import MastraAgentModel, MastraProject, MastraToolModel, MemoryModel, WorkflowModel


# ─────────────────────── Jinja2 Setup ───────────────────────

def _create_jinja_env() -> Environment:
    """Create Jinja2 environment with templates directory."""
    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    
    # Custom filter: escape for TypeScript template-literal strings and single-line comments
    def _ts_escape(s: str) -> str:
        if not s:
            return ""
        return (s.replace("\\", "\\\\")
                 .replace("`", "\\`")
                 .replace("${", "\\${"))
    
    # Custom filter: safe single-line version — strips newlines for use in // comments
    def _ts_comment(s: str) -> str:
        if not s:
            return ""
        # Collapse to single line, escape backtick-critical chars
        single = s.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        return single.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${") 
    
    env.filters["ts_escape"] = _ts_escape
    env.filters["ts_comment"] = _ts_comment

    # Custom filter: turn a raw task description into a TS template literal body,
    # converting CrewAI-style {field_name} placeholders into real `${context.field_name
    # ?? ''}` interpolations against a step's local `context` object, instead of
    # leaving them as inert literal text the agent has no real value for.
    import re as _re

    def _ts_interpolate(s: str, var: str = "context") -> str:
        if not s:
            return ""
        escaped = s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        return _re.sub(
            r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}",
            lambda m: f"${{{var}.{m.group(1)} ?? ''}}",
            escaped,
        )

    env.filters["ts_interpolate"] = _ts_interpolate

    # Custom filter: escape for JSON string values
    def _json_escape(s: str) -> str:
        if not s:
            return ""
        return (s.replace("\\", "\\\\")
                 .replace('"', '\\"')
                 .replace("\n", "\\n")
                 .replace("\r", "\\r")
                 .replace("\t", "\\t"))
    
    env.filters["json_escape"] = _json_escape
    
    return env


# ─────────────────────── Dependency Inference ───────────────────────

def _infer_dependencies(project: MastraProject) -> Dict[str, str]:
    """
    Infer npm dependencies from project components.
    
    Returns dict of package_name → version.
    """
    deps = {
        "@mastra/core": "latest",  # Always required
        "zod": "^3.23.0",          # Always required for schemas
    }
    
    # Check for memory usage
    if project.memory_configs:
        deps["@mastra/memory"] = "latest"

        # Storage backends
        for mem in project.memory_configs:
            if mem.storage_type == "mongodb":
                deps["@mastra/mongodb"] = "latest"
            elif mem.storage_type == "pg":
                deps["@mastra/pg"] = "latest"
            elif mem.storage_type == "upstash":
                deps["@mastra/upstash"] = "latest"
            # libsql uses @mastra/libsql
            elif mem.storage_type == "libsql":
                deps["@mastra/libsql"] = "latest"
    
    # Check for specific LLM providers (for embeddings etc.)
    providers_used = set()
    for llm in project.language_models:
        if llm.provider:
            providers_used.add(llm.provider.lower())
    
    return deps


def _infer_dev_dependencies() -> Dict[str, str]:
    """Infer dev dependencies (TypeScript, etc.)."""
    return {
        "typescript": "^5.0.0",
        "tsx": "^4.0.0",
        "@types/node": "^20.0.0",
        "mastra": "latest",  # Required for 'mastra dev' command
    }


# ─────────────────────── Memory Helpers ───────────────────────

# Mapping of storage_type → TypeScript storage class + import package
_STORAGE_CLASS_MAP: Dict[str, Dict[str, str]] = {
    "mongodb": {
        "class": "MongoDBStore",
        "package": "@mastra/mongodb",
    },
    "pg": {
        "class": "PostgresStore",
        "package": "@mastra/pg",
    },
    "libsql": {
        "class": "LibSQLStore",
        "package": "@mastra/libsql",
    },
    "upstash": {
        "class": "UpstashStore",
        "package": "@mastra/upstash",
    },
}

_VECTOR_CLASS_MAP: Dict[str, Dict[str, str]] = {
    "pgvector": {
        "class": "PgVector",
        "package": "@mastra/pg",
    },
    "mongodbvector": {
        "class": "MongoDBVector",
        "package": "@mastra/mongodb",
    },
    "libsqlvector": {
        "class": "LibSQLVector",
        "package": "@mastra/libsql",
    },
}

# Default env-var placeholders per storage type when no explicit URL is found
_STORAGE_DEFAULT_CONFIGS: Dict[str, List[Dict[str, str]]] = {
    "mongodb": [
        {"key": "id", "value": "'mastra-mongodb-store'"},
        {"key": "url", "value": "process.env.MONGODB_URI!"},
        {"key": "dbName", "value": "process.env.MONGODB_DB_NAME ?? 'mastra_memory'"},
    ],
    "pg": [
        {"key": "id", "value": "'mastra-pg-store'"},
        {"key": "connectionString", "value": "process.env.POSTGRES_URL!"},
    ],
    "libsql": [
        {"key": "id", "value": "'mastra-libsql-store'"},
        {"key": "url", "value": "process.env.DATABASE_URL ?? 'file:local.db'"},
    ],
    "upstash": [
        {"key": "id", "value": "'mastra-upstash-store'"},
        {"key": "url", "value": "process.env.UPSTASH_REDIS_REST_URL!"},
        {"key": "token", "value": "process.env.UPSTASH_REDIS_REST_TOKEN!"},
    ],
}


def _storage_class(mem: MemoryModel) -> str:
    """Return TypeScript storage class name for this memory."""
    return _STORAGE_CLASS_MAP.get(mem.storage_type, {"class": "LibSQLStore"})["class"]


def _storage_package(mem: MemoryModel) -> str:
    """Return npm package for this memory's storage backend."""
    return _STORAGE_CLASS_MAP.get(mem.storage_type, {"package": "@mastra/libsql"})["package"]


def _quote_js_value(val: str) -> str:
    """Return val as a TS expression: unquoted if it's already a JS expression
    (process.env.*, a numeric literal, or a call expression like
    `openai.embedding('text-embedding-3-small')`), single-quoted string literal
    otherwise.
    """
    stripped = val.strip()
    if (
        stripped.startswith("process.env")
        or stripped.lstrip("-").isdigit()
        or re.match(r'^[A-Za-z_$][\w$]*(\.[A-Za-z_$][\w$]*)*\(', stripped)
    ):
        return stripped
    # String literal — escape any single quotes inside the value
    inner = stripped.replace("'", "\\'")
    return f"'{inner}'"


def _storage_config_entries(mem: MemoryModel) -> List[Dict[str, str]]:
    """
    Return list of {key, value} dicts for the storage constructor.

    Prefers explicit values from the KG; falls back to env-var placeholders.
    Values that are JavaScript expressions (process.env.*, numeric) are kept
    as-is; everything else is quoted as a TypeScript string literal.

    Keys that contain dots or other characters invalid in bare JS identifiers
    are wrapped in double-quotes so they render as valid object literal keys.
    """
    def _safe_key(k: str) -> str:
        """Return k as a valid TypeScript object-literal key.

        Bare identifier: letters, digits, $ and _ only, not starting with digit.
        Anything else (e.g. contains '.') must be quoted.
        """
        if re.match(r'^[A-Za-z_$][A-Za-z0-9_$]*$', k):
            return k
        # Escape any double-quotes inside the key itself
        escaped = k.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'

    if mem.storage_config:
        entries = [{"key": _safe_key(cfg.key), "value": _quote_js_value(cfg.value)} for cfg in mem.storage_config]
        # Always ensure 'id' is present for all storage types (required by modern Mastra stores)
        if not any(e["key"] == "id" for e in entries):
            store_id = f"mastra-{mem.storage_type}-store"
            entries.insert(0, {"key": "id", "value": f"'{store_id}'"})
        return entries

    # No explicit config — return defaults (already contain process.env or literals)
    return _STORAGE_DEFAULT_CONFIGS.get(mem.storage_type, _STORAGE_DEFAULT_CONFIGS["libsql"])


def _vector_class(mem: MemoryModel) -> str:
    """Return TypeScript vector store class name (empty string if none)."""
    if not mem.vector_type:
        return ""
    return _VECTOR_CLASS_MAP.get(mem.vector_type, {}).get("class", "")


def _vector_package(mem: MemoryModel) -> str:
    """Return npm package for this memory's vector store backend."""
    if not mem.vector_type:
        return ""
    return _VECTOR_CLASS_MAP.get(mem.vector_type, {}).get("package", "")


def _vector_config_entries(mem: MemoryModel) -> List[Dict[str, str]]:
    """Return list of {key, value} dicts for the vector store constructor."""
    if mem.vector_config:
        return [{"key": cfg.key, "value": _quote_js_value(cfg.value)} for cfg in mem.vector_config]
    return []


import re


def _extract_zod_field_names(schema: Optional[str]) -> List[str]:
    """Pull top-level field names out of a "z.object({a: z.string(), ...})" string.

    Used to give execute() bodies a concrete list of keys to read/write,
    since the schema itself is stored as an opaque rendered string, not a
    structured field list.
    """
    if not schema:
        return []
    return re.findall(r"(\w+):\s*z\.", schema)


def _is_all_string_schema(schema: Optional[str]) -> bool:
    """True if every field in the schema is z.string() (or there are no fields).

    The real execute() body codegen casts inputData to Record<string, string>
    and writes result.text (a string) into any missing output field — correct
    only when every field really is a string. Some Mastra-native schemas have
    genuinely non-string fields (e.g. `incrementedValue: z.number()`, from
    _schema_from_json_like/_to_zod_type), where that cast and assignment
    would produce code that fails to typecheck. Route those to the safer stub
    instead of guessing at a numeric/boolean/array default value.
    """
    if not schema:
        return True
    types = re.findall(r"\w+:\s*z\.(\w+)", schema)
    return all(t == "string" for t in types)


def _sanitize_zod_schema(schema: Optional[str]) -> Optional[str]:
    """
    Sanitize Zod schema strings extracted from the KG.

    Fixes common issues:
      - `field?: z.type()` → `field: z.optional(z.type())`
        (TypeScript object member optional syntax is invalid in Zod object literals)
    """
    if not schema:
        return schema
    # Replace `identifier?: z.something` with `identifier: z.optional(z.something`
    # We match 'word?:' and convert to 'word: z.optional('
    # Then we need to close the paren — approximate by wrapping the rest up to '}' or ','
    # Simple approach: just strip the '?' from property names in z.object({...})
    sanitized = re.sub(r'(\w+)\?\s*:', r'\1:', schema)
    return sanitized


# ─────────────────────── File Generators ───────────────────────

def _clear_stale_files(directory: Path) -> None:
    """Removes .ts files left in directory from an earlier generator run."""
    if not directory.exists():
        return
    for path in directory.glob("*.ts"):
        path.unlink()


def generate_project(project: MastraProject, output_dir: str) -> str:
    """
    Generate complete Mastra AI TypeScript project directory.
    
    Args:
        project: MastraProject IR from extraction layer
        output_dir: Base output directory path
        
    Returns:
        Full path to generated project directory
    """
    project_dir = Path(output_dir) / project.project_var_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create src/mastra directory structure
    mastra_dir = project_dir / "src" / "mastra"
    mastra_dir.mkdir(parents=True, exist_ok=True)
    
    (mastra_dir / "agents").mkdir(exist_ok=True)
    (mastra_dir / "tools").mkdir(exist_ok=True)
    (mastra_dir / "workflows").mkdir(exist_ok=True)
    if project.memory_configs:
        (mastra_dir / "memory").mkdir(exist_ok=True)

    # Clear stale files left over from a previous run against this same output
    # directory (e.g. a renamed/removed tool or workflow) so they don't linger
    # with imports that no longer resolve against the freshly generated index.ts.
    _clear_stale_files(mastra_dir / "agents")
    _clear_stale_files(mastra_dir / "tools")
    _clear_stale_files(mastra_dir / "workflows")
    _clear_stale_files(mastra_dir / "memory")

    # Generate files
    _generate_index_ts(project, mastra_dir)
    _generate_agent_files(project, mastra_dir / "agents")
    _generate_tool_files(project, mastra_dir / "tools")
    _generate_workflow_files(project, mastra_dir / "workflows")
    _generate_ad_hoc_tasks(project, mastra_dir / "workflows")
    _generate_agents_index(project, mastra_dir / "agents")
    _generate_tools_index(project, mastra_dir / "tools")
    _generate_workflows_index(project, mastra_dir / "workflows")
    if project.memory_configs:
        _generate_memory_files(project, mastra_dir / "memory")
        _generate_memory_index(project, mastra_dir / "memory")
    
    _generate_package_json(project, project_dir)
    _generate_tsconfig_json(project, project_dir)
    _generate_env_example(project, project_dir)
    _generate_readme(project, project_dir)
    _generate_run_ts(project, project_dir)

    return str(project_dir)


def _generate_index_ts(project: MastraProject, mastra_dir: Path) -> None:
    """Generate src/mastra/index.ts - Mastra instance + registrations."""
    env = _create_jinja_env()
    template = env.get_template("index.ts.j2")
    
    content = template.render(
        project=project,
        agents=project.agents,
        workflows=project.workflows,
        memory_configs=project.memory_configs,
    )
    
    (mastra_dir / "index.ts").write_text(content, encoding="utf-8")


def _generate_agent_files(project: MastraProject, agents_dir: Path) -> None:
    """Generate per-agent TypeScript files."""
    env = _create_jinja_env()
    template = env.get_template("agent.ts.j2")
    
    for agent in project.agents:
        content = template.render(
            agent=agent,
            project=project,
        )
        
        file_path = agents_dir / f"{agent.var_name}.ts"
        file_path.write_text(content, encoding="utf-8")


def _generate_agents_index(project: MastraProject, agents_dir: Path) -> None:
    """Generate src/mastra/agents/index.ts export barrel."""
    env = _create_jinja_env()
    template = env.get_template("agents.index.ts.j2")
    content = template.render(agents=project.agents)
    (agents_dir / "index.ts").write_text(content, encoding="utf-8")


def _generate_tool_files(project: MastraProject, tools_dir: Path) -> None:
    """Generate per-tool TypeScript files with createTool(). Skip storage tools."""
    env = _create_jinja_env()
    template = env.get_template("tool.ts.j2")
    
    for tool in project.tools:
        if tool.is_storage_tool:
            continue  # Storage backends are not real tools

        # Sanitize schemas: fix invalid '?:' optional syntax from KG extraction
        tool_for_render = tool.model_copy(update={
            "input_schema": _sanitize_zod_schema(tool.input_schema),
            "output_schema": _sanitize_zod_schema(tool.output_schema),
        })

        content = template.render(tool=tool_for_render)

        file_path = tools_dir / f"{tool.var_name}.ts"
        file_path.write_text(content, encoding="utf-8")


def _generate_tools_index(project: MastraProject, tools_dir: Path) -> None:
    """Generate src/mastra/tools/index.ts export barrel."""
    env = _create_jinja_env()
    template = env.get_template("tools.index.ts.j2")
    content = template.render(tools=project.tools)
    (tools_dir / "index.ts").write_text(content, encoding="utf-8")


def _generate_workflow_files(project: MastraProject, workflows_dir: Path) -> None:
    """Generate per-workflow TypeScript files. (Milestone 2+)"""
    if not project.workflows:
        return
    
    env = _create_jinja_env()
    template = env.get_template("workflow.ts.j2")
    
    for workflow in project.workflows:
        sanitized_steps = []
        for step in workflow.steps:
            sanitized_steps.append(step.model_copy(update={
                "input_schema": _sanitize_zod_schema(step.input_schema),
                "output_schema": _sanitize_zod_schema(step.output_schema),
                "suspend_schema": _sanitize_zod_schema(step.suspend_schema),
                "resume_schema": _sanitize_zod_schema(step.resume_schema),
            }))

        wf_input_schema = _sanitize_zod_schema(workflow.input_schema)
        wf_output_schema = _sanitize_zod_schema(workflow.output_schema)

        # For `.then()`-chained workflows (everything except `.parallel([...])`),
        # Mastra type-checks that each step's inputSchema is assignable from the
        # previous step's outputSchema, and the first step's from the workflow
        # input. Step output schemas aren't extracted from the KG (they default
        # to `z.object({})`), so any step with a non-empty inputSchema breaks the
        # chain. Rewrite each step's outputSchema to the next step's inputSchema
        # (a reasonable scaffold assumption: a step produces what the next one
        # consumes) and align the workflow input/output with the chain endpoints,
        # while preserving each step's declared inputSchema for fidelity.
        if sanitized_steps and workflow.control_flow.value != "parallel":
            chained_steps = []
            for idx, step in enumerate(sanitized_steps):
                if idx + 1 < len(sanitized_steps):
                    next_input = sanitized_steps[idx + 1].input_schema
                    chained_steps.append(step.model_copy(update={"output_schema": next_input}))
                else:
                    chained_steps.append(step)
            sanitized_steps = chained_steps
            wf_input_schema = sanitized_steps[0].input_schema
            wf_output_schema = sanitized_steps[-1].output_schema

        sanitized_steps = [
            step.model_copy(update={
                "input_fields": _extract_zod_field_names(step.input_schema),
                "output_fields": _extract_zod_field_names(step.output_schema),
                "schema_all_string": (
                    _is_all_string_schema(step.input_schema)
                    and _is_all_string_schema(step.output_schema)
                ),
            })
            for step in sanitized_steps
        ]

        workflow_for_render = workflow.model_copy(update={
            "input_schema": wf_input_schema,
            "output_schema": wf_output_schema,
            "steps": sanitized_steps,
        })

        content = template.render(
            workflow=workflow_for_render,
            project=project,
        )
        
        file_path = workflows_dir / f"{workflow.var_name}.ts"
        file_path.write_text(content, encoding="utf-8")


def _generate_workflows_index(project: MastraProject, workflows_dir: Path) -> None:
    """Generate src/mastra/workflows/index.ts export barrel."""
    env = _create_jinja_env()
    template = env.get_template("workflows.index.ts.j2")
    content = template.render(workflows=project.workflows)
    (workflows_dir / "index.ts").write_text(content, encoding="utf-8")


def _generate_memory_files(project: MastraProject, memory_dir: Path) -> None:
    """Generate per-memory TypeScript files. (Milestone 3+)"""
    env = _create_jinja_env()
    template = env.get_template("memory.ts.j2")

    for mem in project.memory_configs:
        mem_for_render = mem.model_copy(update={
            "embedder_model": _quote_js_value(mem.embedder_model) if mem.embedder_model else mem.embedder_model,
        })
        content = template.render(
            memory=mem_for_render,
            storage_class=_storage_class(mem),
            storage_package=_storage_package(mem),
            storage_config_entries=_storage_config_entries(mem),
            vector_class=_vector_class(mem),
            vector_package=_vector_package(mem),
            vector_config_entries=_vector_config_entries(mem),
        )

        file_path = memory_dir / f"{mem.var_name}.ts"
        file_path.write_text(content, encoding="utf-8")


def _generate_memory_index(project: MastraProject, memory_dir: Path) -> None:
    """Generate src/mastra/memory/index.ts export barrel."""
    env = _create_jinja_env()
    template = env.get_template("memory.index.ts.j2")
    content = template.render(memory_configs=project.memory_configs)
    (memory_dir / "index.ts").write_text(content, encoding="utf-8")


def _generate_package_json(project: MastraProject, project_dir: Path) -> None:
    """Generate package.json with auto-inferred dependencies."""
    env = _create_jinja_env()
    template = env.get_template("package.json.j2")
    
    dependencies = _infer_dependencies(project)
    dev_dependencies = _infer_dev_dependencies()
    
    content = template.render(
        project_name=project.project_var_name,
        project_description=project.description,
        dependencies=dependencies,
        dev_dependencies=dev_dependencies,
        has_run_ts=bool(project.workflows),
    )

    (project_dir / "package.json").write_text(content, encoding="utf-8")


def _generate_tsconfig_json(project: MastraProject, project_dir: Path) -> None:
    """Generate tsconfig.json - TypeScript configuration."""
    env = _create_jinja_env()
    template = env.get_template("tsconfig.json.j2")
    
    content = template.render()
    
    (project_dir / "tsconfig.json").write_text(content, encoding="utf-8")


def _generate_env_example(project: MastraProject, project_dir: Path) -> None:
    """Generate .env.example with required API keys."""
    env = _create_jinja_env()
    template = env.get_template("env.example.j2")
    
    # Collect required env vars
    providers_used = set()
    for llm in project.language_models:
        if llm.provider:
            providers_used.add(llm.provider.lower())
    
    # Provider → env var mapping
    provider_vars = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "cohere": "COHERE_API_KEY",
        "groq": "GROQ_API_KEY",
    }
    
    env_vars = []
    for provider in sorted(providers_used):
        if provider in provider_vars:
            var_name = provider_vars[provider]
            if var_name not in [v["key"] for v in env_vars]:
                env_vars.append({
                    "key": var_name,
                    "value": f"your_{var_name.lower()}_here",
                    "comment": f"{provider.capitalize()} API key"
                })
    
    # Add storage-specific vars
    for mem in project.memory_configs:
        if mem.storage_type == "mongodb":
            if not any(v["key"] == "MONGODB_URI" for v in env_vars):
                env_vars.append({
                    "key": "MONGODB_URI",
                    "value": "mongodb://localhost:27017",
                    "comment": "MongoDB connection URI"
                })
            if not any(v["key"] == "MONGODB_DB_NAME" for v in env_vars):
                env_vars.append({
                    "key": "MONGODB_DB_NAME",
                    "value": "mastra_memory",
                    "comment": "MongoDB database name"
                })
        elif mem.storage_type == "pg":
            if not any(v["key"] == "POSTGRES_URL" for v in env_vars):
                env_vars.append({
                    "key": "POSTGRES_URL",
                    "value": "postgresql://postgres:postgres@localhost:5432/mastra",
                    "comment": "PostgreSQL connection URL"
                })
        elif mem.storage_type == "libsql":
            if not any(v["key"] == "DATABASE_URL" for v in env_vars):
                env_vars.append({
                    "key": "DATABASE_URL",
                    "value": "file:local.db",
                    "comment": "LibSQL database URL"
                })
        elif mem.storage_type == "upstash":
            if not any(v["key"] == "UPSTASH_REDIS_REST_URL" for v in env_vars):
                env_vars.append({
                    "key": "UPSTASH_REDIS_REST_URL",
                    "value": "https://your-upstash-url.upstash.io",
                    "comment": "Upstash Redis REST URL"
                })
            if not any(v["key"] == "UPSTASH_REDIS_REST_TOKEN" for v in env_vars):
                env_vars.append({
                    "key": "UPSTASH_REDIS_REST_TOKEN",
                    "value": "your_upstash_token",
                    "comment": "Upstash Redis REST token"
                })
    
    # Default: always include OPENAI_API_KEY
    if not any(v["key"] == "OPENAI_API_KEY" for v in env_vars):
        env_vars.insert(0, {
            "key": "OPENAI_API_KEY",
            "value": "your_openai_api_key_here",
            "comment": "OpenAI API key (default LLM provider)"
        })
    
    content = template.render(env_vars=env_vars)
    
    (project_dir / ".env.example").write_text(content, encoding="utf-8")


def _generate_readme(project: MastraProject, project_dir: Path) -> None:
    """Generate README.md with project documentation."""
    env = _create_jinja_env()
    template = env.get_template("README.md.j2")
    
    content = template.render(
        project_name=project.project_name,
        description=project.description,
        agents=project.agents,
        tools=project.tools,
        workflows=project.workflows,
    )
    
    (project_dir / "README.md").write_text(content, encoding="utf-8")


def _generate_run_ts(project: MastraProject, project_dir: Path) -> None:
    """Generate run.ts - a driver that actually executes the project's workflows."""
    if not project.workflows:
        return

    env = _create_jinja_env()
    template = env.get_template("run.ts.j2")

    workflows_ctx = []
    for wf in project.workflows:
        first_step = wf.steps[0] if wf.steps else None
        seed_fields = (
            _extract_zod_field_names(_sanitize_zod_schema(first_step.input_schema))
            if first_step else []
        )
        workflows_ctx.append({"var_name": wf.var_name, "seed_fields": seed_fields})

    content = template.render(workflows=workflows_ctx)
    (project_dir / "run.ts").write_text(content, encoding="utf-8")


def _generate_ad_hoc_tasks(project: MastraProject, workflows_dir: Path) -> None:
    """Generate standalone ad-hoc tasks as createStep steps."""
    workflow_task_iris = set()
    for wf in project.workflows:
        for step in wf.steps:
            if step.task_iri:
                workflow_task_iris.add(step.task_iri)

    ad_hoc_tasks = [
        task for task in project.tasks
        if task.iri not in workflow_task_iris
    ]

    # Always write the file (it will be empty of steps if there are no ad-hoc tasks)
    env = _create_jinja_env()
    template = env.get_template("ad_hoc_tasks.ts.j2")
    content = template.render(tasks=ad_hoc_tasks)
    (workflows_dir / "ad_hoc_tasks.ts").write_text(content, encoding="utf-8")
