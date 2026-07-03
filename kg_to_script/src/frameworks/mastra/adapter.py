"""Mastra adapter: maps AgenticProject -> MastraProject."""

from __future__ import annotations

import json
import re
from typing import Dict, List, Optional, Tuple

from ...core.helpers import camel
from ...core.models import AgenticProject, WorkflowType
from .models import (
    ConfigModel,
    ControlFlowType,
    LanguageModelModel,
    MastraAgentModel,
    MastraProject,
    MastraToolModel,
    MemoryModel,
    StepModel,
    ToolConfigModel,
    WorkflowModel,
)


def _to_kebab(name: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", name or "")
    clean = re.sub(r"-+", "-", clean).strip("-").lower()
    return clean or "mastra-project"


def _to_camel(name: str) -> str:
    if not name:
        return "unnamed"
    parts = re.split(r"[^a-zA-Z0-9]+", name)
    parts = [p for p in parts if p]
    if not parts:
        return "unnamed"
    head = parts[0].lower()
    tail = "".join(p[:1].upper() + p[1:] for p in parts[1:])
    out = head + tail
    if out and out[0].isdigit():
        out = f"item{out}"
    return out


def _unique_var_name(base: str, used: set) -> str:
    """Disambiguate `base` against names already in `used`, then reserve it.

    Multiple agents/tools/workflows can map to the same camelCase name (e.g.
    two unnamed AutoGen agents both become "unnamed"), which would otherwise
    collide as duplicate TS identifiers and overwrite each other's files.
    """
    name = base
    suffix = 2
    while name in used:
        name = f"{base}{suffix}"
        suffix += 1
    used.add(name)
    return name


def _safe_schema_key(name: str) -> str:
    key = re.sub(r"[^a-zA-Z0-9_]+", "_", name or "").strip("_")
    if not key:
        return "value"
    if key[0].isdigit():
        key = f"field_{key}"
    return key


def _to_zod_type(type_hint: str) -> str:
    text = (type_hint or "").lower()
    if any(t in text for t in ["bool", "true/false", "boolean"]):
        return "z.boolean()"
    if any(t in text for t in ["int", "float", "double", "number"]):
        return "z.number()"
    if "array" in text or "list" in text:
        return "z.array(z.string())"
    if "object" in text or "json" in text:
        return "z.object({})"
    return "z.string()"


def _object_schema_from_fields(fields: List[Tuple[str, str]]) -> Optional[str]:
    normalized: List[Tuple[str, str]] = []
    seen = set()
    for name, zod_type in fields:
        key = _safe_schema_key(name)
        if key in seen:
            continue
        seen.add(key)
        normalized.append((key, zod_type))
    if not normalized:
        return None
    entries = ", ".join([f"{name}: {zod_type}" for name, zod_type in normalized])
    return f"z.object({{{entries}}})"


def _schema_from_placeholders(text: str) -> Optional[str]:
    names = re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", text or "")
    return _object_schema_from_fields([(n, "z.string()") for n in names])


def _schema_from_json_like(text: str) -> Optional[str]:
    raw = (text or "").strip()
    if not raw:
        return None

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z]*", "", raw).strip()
        raw = raw[:-3].strip() if raw.endswith("```") else raw

    try:
        parsed = json.loads(raw)
    except Exception:
        return None

    if isinstance(parsed, dict):
        fields = []
        for key, val in parsed.items():
            if isinstance(val, bool):
                fields.append((str(key), "z.boolean()"))
            elif isinstance(val, (int, float)):
                fields.append((str(key), "z.number()"))
            elif isinstance(val, list):
                fields.append((str(key), "z.array(z.string())"))
            elif isinstance(val, dict):
                fields.append((str(key), "z.object({})"))
            else:
                fields.append((str(key), "z.string()"))
        return _object_schema_from_fields(fields)
    if isinstance(parsed, list):
        return "z.array(z.string())"
    return "z.string()"


def _schema_from_inline_field_hints(text: str) -> Optional[str]:
    lines = (text or "").splitlines()
    fields: List[Tuple[str, str]] = []
    for line in lines:
        match = re.search(r"([a-zA-Z_][a-zA-Z0-9_\- ]*)\s*[:=-]\s*([a-zA-Z][a-zA-Z0-9_/ -]*)", line)
        if not match:
            continue
        field_name = match.group(1).strip().replace("-", "_").replace(" ", "_")
        type_hint = match.group(2).strip()
        fields.append((field_name, _to_zod_type(type_hint)))
    return _object_schema_from_fields(fields)


def _schema_from_prompt(raw: str) -> Optional[str]:
    text = (raw or "").strip()
    if not text:
        return None
    if text.startswith("z.") or "z.object(" in text or "z.array(" in text:
        return text
    for builder in (_schema_from_json_like, _schema_from_inline_field_hints, _schema_from_placeholders):
        schema = builder(text)
        if schema:
            return schema
    return None


def _infer_provider_model(name: str, description: str) -> Tuple[str, str]:
    text = f"{name} {description}".lower()

    if "anthropic" in text or "claude" in text:
        provider = "anthropic"
    elif "google" in text or "gemini" in text:
        provider = "google"
    elif "groq" in text:
        provider = "groq"
    elif "cohere" in text:
        provider = "cohere"
    else:
        provider = "openai"

    model_match = re.search(
        r"(gpt-[a-z0-9._-]+|o[134](?:-mini)?|claude-[a-z0-9._-]+|gemini-[a-z0-9._-]+)",
        text,
    )
    if model_match:
        model_name = model_match.group(1)
    elif provider == "anthropic":
        model_name = "claude-3-5-sonnet-latest"
    elif provider == "google":
        model_name = "gemini-2.0-flash"
    else:
        model_name = "gpt-4o-mini"

    return provider, model_name


def _map_language_models(project: AgenticProject) -> Dict[str, LanguageModelModel]:
    mapped: Dict[str, LanguageModelModel] = {}
    for lm in project.language_models:
        provider = lm.provider.strip().lower() if lm.provider else ""
        model_name = lm.model_name.strip() if lm.model_name else ""
        if not provider or not model_name:
            inferred_provider, inferred_model = _infer_provider_model(lm.name, lm.description)
            provider = provider or inferred_provider
            model_name = model_name or inferred_model

        mapped[lm.iri] = LanguageModelModel(
            iri=lm.iri,
            name=lm.name,
            description=lm.description,
            provider=provider,
            model_name=model_name,
        )
    return mapped


def _map_tools(project: AgenticProject) -> Tuple[Dict[str, MastraToolModel], Dict[str, str]]:
    tools_by_iri: Dict[str, MastraToolModel] = {}
    iri_to_var: Dict[str, str] = {}
    tasks_by_tool: Dict[str, List] = {}
    used_var_names: set = set()

    for task in project.tasks:
        if task.performed_by_iri:
            tasks_by_tool.setdefault(task.performed_by_iri, []).append(task)

    for tool in project.tools:
        var_name = _unique_var_name(_to_camel(tool.var_name), used_var_names)
        related_tasks = tasks_by_tool.get(tool.iri, [])
        input_schema = None
        output_schema = None

        for cfg in tool.configs:
            if not input_schema and "input" in cfg.key.lower() and "schema" in cfg.key.lower():
                input_schema = _schema_from_prompt(cfg.value)
            if not output_schema and "output" in cfg.key.lower() and "schema" in cfg.key.lower():
                output_schema = _schema_from_prompt(cfg.value)

        for task in related_tasks:
            input_schema = input_schema or _schema_from_prompt(task.prompt_input_data)
            output_schema = output_schema or _schema_from_prompt(task.prompt_output_indicator)

        if not input_schema:
            input_schema = _schema_from_prompt(tool.description)
        if not output_schema:
            output_schema = _schema_from_prompt(
                "\n".join(t.prompt_output_indicator for t in related_tasks if t.prompt_output_indicator)
            )

        iri_to_var[tool.iri] = var_name
        tools_by_iri[tool.iri] = MastraToolModel(
            iri=tool.iri,
            var_name=var_name,
            tool_id=tool.label or var_name,
            description=tool.description or "",
            input_schema=input_schema,
            output_schema=output_schema,
            execute_description=tool.description or "",
            configs=[ToolConfigModel(key=c.key, value=c.value) for c in tool.configs],
            capabilities=list(tool.capability_iris),
        )

    return tools_by_iri, iri_to_var


def _detect_storage_type(configs: Dict[str, str]) -> str:
    keys = " ".join(k.lower() for k in configs.keys())
    values = " ".join(v.lower() for v in configs.values())
    text = f"{keys} {values}"
    if "mongo" in text:
        return "mongodb"
    if "postgres" in text or "pgvector" in text or "connectionstring" in keys:
        return "pg"
    if "upstash" in text or "redis" in text:
        return "upstash"
    if "libsql" in text or "turso" in text or "database_url" in keys:
        return "libsql"
    return "libsql"


# ---------------------------------------------------------------------------
# Memory option key aliases — all map to typed MemoryModel fields
# ---------------------------------------------------------------------------
_MEMORY_OPTION_KEYS: Dict[str, str] = {
    # lastMessages
    "lastmessages": "last_messages",
    "last_messages": "last_messages",
    # semanticRecall simple boolean disable
    "semanticrecall": "semanticRecall_flag",
    "semantic_recall": "semanticRecall_flag",
    # semanticRecall.topK
    "semanticrecall.topk": "semantic_recall_top_k",
    "semanticrecall_topk": "semantic_recall_top_k",
    # semanticRecall.messageRange
    "semanticrecall.messagerange": "semantic_recall_message_range",
    "semanticrecall_messagerange": "semantic_recall_message_range",
    # workingMemory.enabled
    "workingmemory.enabled": "working_memory_enabled",
    "workingmemory_enabled": "working_memory_enabled",
    # workingMemory.scope
    "workingmemory.scope": "working_memory_scope",
    "workingmemory_scope": "working_memory_scope",
    # workingMemory.template
    "workingmemory.template": "working_memory_template",
    "workingmemory_template": "working_memory_template",
    # embedder / memory.embedder.model
    "embedder": "embedder_model",
    "memory.embedder.model": "embedder_model",
    "memory.embedder": "embedder_model",
    # TokenLimiter
    "tokenlimiter": "token_limit",
    "token_limiter": "token_limit",
}

# Keys that must be silently discarded — they are not typed memory option fields
# AND are not valid storage constructor keys. Including them in storage_config
# would cause TypeScript TS2353 "does not exist in type" errors.
_MEMORY_DISCARD_KEYS: set = {
    # Mastra Memory-level toggles that don't belong in LibSQLStore / PgStore etc.
    "threads.generatetitle",
    "threads_generatetitle",
    # Inline JSON blob encoding of all memory options — never a storage key
    "memory.options",
    "memory_options",
    # Resource / thread identifiers passed at runtime, not at construction time
    "memory.resource",
    "memory_resource",
    "memory.thread",
    "memory_thread",
    "resource",
    "thread",
}

# Prefixes that identify storage-backend keys; strip prefix to get clean key.
_STORAGE_KEY_PREFIXES = (
    "storage.",
    "memory.storage.",
)

# Prefixes that belong to storage and should not become typed option fields.
_STORAGE_RAW_PREFIXES = (
    "storage.",
    "memory.storage.",
    "storage_",
)


def _map_memories(project: AgenticProject) -> Dict[str, MemoryModel]:
    """Map each core MemoryModel into Mastra-specific MemoryModel.

    Parses raw KG config keys into typed fields:
    - Memory option keys (lastMessages, semanticRecall.*, workingMemory.*)
      are mapped to typed fields and excluded from storage_config.
    - Storage-prefixed keys (storage.url, memory.storage.id …) have their
      prefix stripped and are passed into storage_config as clean keys.
    - Any remaining unknown keys that aren't option keys go into storage_config
      verbatim so no information is lost.
    """
    mapped: Dict[str, MemoryModel] = {}
    used_var_names: set = set()
    for mem in project.memories:
        storage_type = _detect_storage_type(mem.configs)
        storage_config: List[ConfigModel] = []

        # Typed option accumulators
        last_messages: Optional[int] = None
        semantic_recall_enabled: bool = True
        semantic_recall_top_k: Optional[int] = None
        semantic_recall_message_range: Optional[int] = None
        working_memory_enabled: bool = False
        working_memory_scope: Optional[str] = None
        working_memory_template: Optional[str] = None
        embedder_model: Optional[str] = None
        token_limit: Optional[int] = None

        for raw_key, raw_val in mem.configs.items():
            normalised = raw_key.lower().replace("-", "_")

            # ── 1. Check well-known memory option keys ──
            mapped_field = _MEMORY_OPTION_KEYS.get(normalised)

            # ── 0. Discard keys that are invalid in any storage constructor ──
            if normalised in _MEMORY_DISCARD_KEYS:
                continue
            if mapped_field == "last_messages":
                try:
                    last_messages = int(raw_val)
                except (ValueError, TypeError):
                    pass
                continue
            if mapped_field == "semanticRecall_flag":
                if raw_val.strip().lower() in ("false", "0", "no"):
                    semantic_recall_enabled = False
                continue
            if mapped_field == "semantic_recall_top_k":
                try:
                    semantic_recall_top_k = int(raw_val)
                except (ValueError, TypeError):
                    pass
                continue
            if mapped_field == "semantic_recall_message_range":
                try:
                    semantic_recall_message_range = int(raw_val)
                except (ValueError, TypeError):
                    pass
                continue
            if mapped_field == "working_memory_enabled":
                working_memory_enabled = raw_val.strip().lower() not in ("false", "0", "no")
                continue
            if mapped_field == "working_memory_scope":
                working_memory_scope = raw_val.strip()
                continue
            if mapped_field == "working_memory_template":
                working_memory_template = raw_val
                continue
            if mapped_field == "embedder_model":
                embedder_model = raw_val.strip()
                continue
            if mapped_field == "token_limit":
                try:
                    token_limit = int(raw_val)
                except (ValueError, TypeError):
                    pass
                continue

            # ── 2. Strip storage./ memory.storage. prefix ──
            clean_key = raw_key
            for prefix in _STORAGE_KEY_PREFIXES:
                if raw_key.lower().startswith(prefix):
                    clean_key = raw_key[len(prefix):]
                    break

            # ── 3. Add as storage config entry ──
            storage_config.append(ConfigModel(key=clean_key, value=raw_val))

        mapped[mem.iri] = MemoryModel(
            iri=mem.iri,
            var_name=_unique_var_name(_to_camel(mem.var_name), used_var_names),
            label=mem.label,
            description=mem.description,
            storage_type=storage_type,
            storage_config=storage_config,
            last_messages=last_messages,
            semantic_recall_enabled=semantic_recall_enabled,
            semantic_recall_top_k=semantic_recall_top_k,
            semantic_recall_message_range=semantic_recall_message_range,
            working_memory_enabled=working_memory_enabled,
            working_memory_scope=working_memory_scope,
            working_memory_template=working_memory_template,
            embedder_model=embedder_model if embedder_model else None,
            token_limit=token_limit,
        )
    return mapped


def _read_int_config(configs: Dict[str, str], keys: List[str]) -> Optional[int]:
    for key in keys:
        if key in configs:
            try:
                return int(configs[key])
            except ValueError:
                continue
    return None


def _map_agents(
    project: AgenticProject,
    tools_var_by_iri: Dict[str, str],
    language_models_by_iri: Dict[str, LanguageModelModel],
    memory_by_iri: Dict[str, MemoryModel],
) -> Tuple[Dict[str, MastraAgentModel], Dict[str, str]]:
    agents: Dict[str, MastraAgentModel] = {}
    agent_var_by_iri: Dict[str, str] = {}
    used_var_names: set = set()

    for agent in project.agents:
        var_name = _unique_var_name(_to_camel(agent.var_name), used_var_names)
        agent_var_by_iri[agent.iri] = var_name

        llm_obj: Optional[LanguageModelModel] = None
        model_router = "openai/gpt-4o-mini"
        if agent.language_model and agent.language_model.iri in language_models_by_iri:
            llm_obj = language_models_by_iri[agent.language_model.iri]
            model_router = llm_obj.model_router_string

        instructions = (
            agent.system_prompt
            or agent.backstory
            or agent.goal
            or f"You are {agent.role or 'a helpful assistant'}."
        )

        tool_var_names = [
            tools_var_by_iri[t_iri]
            for t_iri in agent.tool_iris
            if t_iri in tools_var_by_iri
        ]

        memory_var_name = None
        for k_iri in agent.knowledge_iris:
            if k_iri in memory_by_iri:
                memory_var_name = memory_by_iri[k_iri].var_name
                break

        agents[agent.iri] = MastraAgentModel(
            iri=agent.iri,
            var_name=var_name,
            agent_id=agent.agent_id or var_name,
            name=agent.role or camel(agent.var_name),
            instructions=instructions,
            model=model_router,
            tool_var_names=tool_var_names,
            memory_var_name=memory_var_name,
            max_retries=_read_int_config(agent.configs, ["max_retries", "maxRetries"]),
            llm=llm_obj,
        )

    return agents, agent_var_by_iri


def _map_control_flow(workflow_type: WorkflowType) -> ControlFlowType:
    if workflow_type == WorkflowType.PARALLEL:
        return ControlFlowType.PARALLEL
    if workflow_type == WorkflowType.BRANCHING:
        return ControlFlowType.BRANCHING
    if workflow_type == WorkflowType.LOOP:
        return ControlFlowType.LOOP
    if workflow_type == WorkflowType.MIXED:
        return ControlFlowType.MIXED
    return ControlFlowType.SEQUENTIAL


def _map_workflows(
    project: AgenticProject,
    agent_var_by_iri: Dict[str, str],
    tool_var_by_iri: Dict[str, str],
) -> List[WorkflowModel]:
    tasks_by_iri = {task.iri: task for task in project.tasks}
    used_workflow_var_names: set = set()
    workflow_var_by_iri = {
        wf.iri: _unique_var_name(
            _to_camel(wf.var_name or wf.label or wf.iri.split("#")[-1]),
            used_workflow_var_names,
        )
        for wf in project.workflows
    }

    workflows: List[WorkflowModel] = []
    for wf in project.workflows:
        steps: List[StepModel] = []
        for step in sorted(wf.steps, key=lambda s: s.step_order):
            task = tasks_by_iri.get(step.task_iri)
            task_label = task.label if task else ""
            # Prefer task_var_name so generated step variable names match KG
            # node names used by the WGI evaluator. Fall back to step.var_name
            # (the raw IRI local-name) only when no task is linked.
            step_name = step.task_var_name or task_label or step.var_name or "step"

            agent_ref = step.agent_iri
            if not agent_ref and task and task.agent_iri:
                agent_ref = task.agent_iri

            tool_var_name = None
            if task and task.performed_by_iri and task.performed_by_iri in tool_var_by_iri:
                tool_var_name = tool_var_by_iri[task.performed_by_iri]

            steps.append(
                StepModel(
                    iri=step.iri,
                    var_name=_to_camel(step_name),
                    step_id=task_label or step_name,
                    step_order=step.step_order,
                    description=step.description or (task.description if task else ""),
                    input_schema=_schema_from_prompt(task.prompt_input_data if task else ""),
                    output_schema=_schema_from_prompt(task.prompt_output_indicator if task else ""),
                    execute_description=(task.prompt_instruction if task else "")
                    or (task.description if task else "")
                    or step.description,
                    task_iri=step.task_iri,
                    agent_var_name=agent_var_by_iri.get(agent_ref, None),
                    tool_var_name=tool_var_name,
                )
            )

        # Deduplicate steps by var_name (same task can be listed under multiple
        # step IRIs in the KG, which would cause TS2451 redeclaration errors).
        seen_var_names: set = set()
        deduped_steps: List[StepModel] = []
        for s in steps:
            if s.var_name not in seen_var_names:
                seen_var_names.add(s.var_name)
                deduped_steps.append(s)
        steps = deduped_steps

        workflows.append(
            WorkflowModel(
                iri=wf.iri,
                var_name=workflow_var_by_iri[wf.iri],
                workflow_id=wf.label or wf.var_name,
                description=wf.description,
                input_schema=(
                    _schema_from_prompt(wf.description)
                    or (steps[0].input_schema if steps else None)
                ),
                output_schema=(steps[-1].output_schema if steps else None),
                steps=steps,
                control_flow=_map_control_flow(wf.workflow_type),
                nested_workflow_var_names=[
                    workflow_var_by_iri[sub_iri]
                    for sub_iri in wf.sub_pattern_iris
                    if sub_iri in workflow_var_by_iri
                ],
            )
        )

    return workflows


def adapt(project: AgenticProject) -> MastraProject:
    """Adapt framework-agnostic AgenticProject into MastraProject."""
    project = project.model_copy(deep=True)

    language_models_by_iri = _map_language_models(project)
    tools_by_iri, tools_var_by_iri = _map_tools(project)
    memory_by_iri = _map_memories(project)
    agents_by_iri, agent_var_by_iri = _map_agents(
        project,
        tools_var_by_iri,
        language_models_by_iri,
        memory_by_iri,
    )
    workflows = _map_workflows(project, agent_var_by_iri, tools_var_by_iri)

    base_name = project.var_name or project.name
    project_var_name = _to_kebab(base_name)
    project_name = camel(re.sub(r"[^a-zA-Z0-9_]", "_", base_name))

    return MastraProject(
        project_name=project_name,
        project_var_name=project_var_name,
        description=project.description,
        agents=list(agents_by_iri.values()),
        tools=list(tools_by_iri.values()),
        workflows=workflows,
        tasks=list(project.tasks),
        memory_configs=list(memory_by_iri.values()),
        language_models=list(language_models_by_iri.values()),
        env_vars=[ConfigModel(key=c.key, value=c.value) for c in project.env_vars],
        system_configs=[
            ConfigModel(key=key, value=value)
            for key, value in project.system_configs.items()
        ],
        goals=[
            {"iri": g.iri, "label": g.label, "description": g.description}
            for g in project.goals
        ],
        objectives=[
            {
                "iri": o.iri,
                "label": o.label,
                "description": o.description,
                "contributes_to_goal": o.contributes_to_goal_iri,
            }
            for o in project.objectives
        ],
        human_agents=[
            {"iri": h.iri, "var_name": h.var_name, "role": h.role}
            for h in project.human_agents
        ],
        environments=[
            {
                "iri": e.iri,
                "label": e.label,
                "description": e.description,
                "env_type": e.env_type,
            }
            for e in project.environments
        ],
        capabilities=[
            {"iri": c.iri, "label": c.label, "description": c.description}
            for c in project.capabilities
        ],
        resources=[
            {"iri": r.iri, "label": r.label, "description": r.description}
            for r in project.resources
        ],
        constraints=[
            {"iri": c.iri, "label": c.label, "description": c.description}
            for c in project.constraints
        ],
    )
