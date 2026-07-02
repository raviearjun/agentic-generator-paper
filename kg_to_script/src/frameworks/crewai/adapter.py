"""CrewAI adapter: maps AgenticProject → CrewProject.

All CrewAI-specific field derivation happens here, keeping the canonical
AgentModel and ToolModel free of framework coupling.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from ...core.models import AgenticProject, TaskModel, WorkflowStepModel
from .models import CrewProject, ProcessType


def _infer_process(project: AgenticProject) -> ProcessType:
    """Determine CrewAI process type from system_configs or workflow topology."""
    process_value = project.system_configs.get("process", "").strip().lower()
    if "hierarchical" in process_value:
        return ProcessType.HIERARCHICAL

    for workflow in project.workflows:
        if workflow.workflow_type.value == "hierarchical":
            return ProcessType.HIERARCHICAL
    return ProcessType.SEQUENTIAL


def _topological_sort_tasks(tasks: List[TaskModel]) -> List[TaskModel]:
    """Sort tasks topologically so that dependencies appear before the tasks that require them."""
    tasks_by_var = {t.var_name: t for t in tasks}
    visited = {}
    sorted_tasks = []

    def visit(task_var: str):
        if visited.get(task_var) == "visiting":
            # Cycle detected; break recursion to avoid infinite loop
            return
        if visited.get(task_var) == "visited":
            return

        visited[task_var] = "visiting"
        task = tasks_by_var.get(task_var)
        if task:
            for dep_var in task.context_task_var_names:
                visit(dep_var)

        visited[task_var] = "visited"
        if task and task not in sorted_tasks:
            sorted_tasks.append(task)

    for task in tasks:
        visit(task.var_name)

    return sorted_tasks


def _flatten_workflow_steps(project: AgenticProject) -> List[WorkflowStepModel]:
    """Collect and deduplicate all workflow steps in step order."""
    if not project.workflows:
        return []

    by_iri: Dict[str, WorkflowStepModel] = {}
    for workflow in project.workflows:
        for step in workflow.steps:
            key = step.iri or f"{workflow.iri}:{step.step_order}:{step.task_iri}"
            if key not in by_iri:
                by_iri[key] = step

    return sorted(by_iri.values(), key=lambda step: step.step_order)


def _derive_allow_delegation(configs: Dict[str, str]) -> Optional[bool]:
    """Read allow_delegation from agent config bag."""
    if "allow_delegation" not in configs:
        return None
    val = configs["allow_delegation"].strip().lower()
    return val in ("true", "1", "yes")


def _derive_verbose(configs: Dict[str, str]) -> Optional[bool]:
    """Read verbose from agent config bag."""
    if "verbose" not in configs:
        return None
    val = configs["verbose"].strip().lower()
    return val not in ("false", "0", "no", "none")


def _derive_tool_class_name(label: str, iri: str) -> str:
    """Derive a CamelCase class name for a tool from its label or IRI fragment."""
    name = label if label else iri.split("/")[-1].split("#")[-1]
    return re.sub(r"[^a-zA-Z0-9]", "", name)


def _infer_llm_provider(lm_name: str, lm_desc: str) -> tuple[str, str]:
    """Infer LLM provider and model_name from label/description text.

    This heuristic only fires here in the CrewAI adapter because CrewAI needs
    a specific provider string to select the right LLM class. Other frameworks
    have their own resolution logic.

    Returns (provider, model_name), both may be empty strings.
    """
    import re as _re
    text = f"{lm_name} {lm_desc}".lower()
    provider = ""
    model_name = ""
    if "ollama" in text:
        provider = "ollama"
        m = _re.search(r"ollama\S*\s*[\(\"']?([a-z0-9._-]+)", text)
        if m:
            model_name = m.group(1)
    elif "openai" in text or "gpt" in text:
        provider = "openai"
        m = _re.search(r"(gpt-[a-z0-9._-]+)", text)
        if m:
            model_name = m.group(1)
    elif "anthropic" in text or "claude" in text:
        provider = "anthropic"
        m = _re.search(r"(claude-[a-z0-9._-]+)", text)
        if m:
            model_name = m.group(1)
    elif "gemini" in text:
        provider = "gemini"
        m = _re.search(r"(gemini-[a-z0-9._-]+)", text)
        if m:
            model_name = m.group(1)
    elif "groq" in text:
        provider = "groq"
    elif "mistral" in text:
        provider = "mistral"
    return provider, model_name


def adapt(project: AgenticProject) -> CrewProject:
    """Adapt framework-agnostic AgenticProject into CrewProject."""
    project = project.model_copy(deep=True)
    tools_by_iri = {tool.iri: tool for tool in project.tools}

    # ── Populate LLM provider/model_name in language_model objects ──
    # This is CrewAI-specific: the generator needs a concrete provider string.
    for lm in project.language_models:
        if not lm.provider:
            provider, model_name = _infer_llm_provider(lm.name, lm.description)
            lm.provider = provider
            if not lm.model_name and model_name:
                lm.model_name = model_name

    # ── Compute per-agent CrewAI derived fields ──
    agent_allow_delegation: Dict[str, Optional[bool]] = {}
    agent_verbose: Dict[str, Optional[bool]] = {}
    agent_tool_var_names: Dict[str, List[str]] = {}

    for agent in project.agents:
        if not agent.role:
            agent.role = "LLM Agent"
        if not agent.goal:
            agent.goal = agent.role
        # Backstory sync
        if not agent.backstory and agent.system_prompt:
            agent.backstory = agent.system_prompt
        if not agent.system_prompt and agent.backstory:
            agent.system_prompt = agent.backstory
        if not agent.backstory:
            agent.backstory = f"You are a {agent.role}."
        if not agent.system_prompt:
            agent.system_prompt = agent.backstory

        # allow_delegation / verbose from config bag
        agent_allow_delegation[agent.var_name] = _derive_allow_delegation(agent.configs)
        agent_verbose[agent.var_name] = _derive_verbose(agent.configs)

        # tool var names
        var_names: List[str] = []
        for tool_iri in agent.tool_iris:
            tool = tools_by_iri.get(tool_iri)
            if tool and tool.var_name not in var_names:
                var_names.append(tool.var_name)
        agent_tool_var_names[agent.var_name] = var_names

        # Resolve agent_var_name for tasks (redundant if extractor already set it)
        # kept as a safety net for KGs that don't use performedByAgent
        agents_by_iri = {a.iri: a for a in project.agents}

    for task in project.tasks:
        if not task.description and task.prompt_instruction:
            task.description = task.prompt_instruction
        if not task.description:
            task.description = task.var_name.replace("_", " ").title()
        if not task.expected_output:
            task.expected_output = f"Completed: {task.var_name}"

        if not task.agent_var_name and task.agent_iri:
            for agent in project.agents:
                if agent.iri == task.agent_iri:
                    task.agent_var_name = agent.var_name
                    break

    # ── Compute per-tool CamelCase class names ──
    tool_class_names: Dict[str, str] = {
        tool.var_name: _derive_tool_class_name(tool.label, tool.iri)
        for tool in project.tools
    }

    workflow_steps = _flatten_workflow_steps(project)
    sorted_tasks = _topological_sort_tasks(project.tasks)

    return CrewProject(
        crew_name=project.name,
        crew_var_name=project.var_name,
        description=project.description,
        process=_infer_process(project),
        agents=project.agents,
        tasks=sorted_tasks,
        tools=project.tools,
        workflow_steps=workflow_steps,
        agent_allow_delegation=agent_allow_delegation,
        agent_verbose=agent_verbose,
        agent_tool_var_names=agent_tool_var_names,
        tool_class_names=tool_class_names,
        language_models=project.language_models,
        env_vars=project.env_vars,
        human_agents=project.human_agents,
        goals=project.goals,
        objectives=project.objectives,
        capabilities=project.capabilities,
        environments=project.environments,
        resources=project.resources,
        constraints=project.constraints,
    )
