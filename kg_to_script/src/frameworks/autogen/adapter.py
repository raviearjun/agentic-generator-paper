from __future__ import annotations

from typing import Dict, List

from ...core.models import AgenticProject, TaskModel
from .models import AutoGenProject


def _resolve_model_name(project: AgenticProject) -> str:
    if project.language_models and project.language_models[0].model_name:
        return project.language_models[0].model_name.strip()
    return "gpt-4o-mini"


def _build_ordered_tasks(project: AgenticProject) -> List[TaskModel]:
    if not project.workflows:
        return list(project.tasks)

    task_by_iri: Dict[str, TaskModel] = {t.iri: t for t in project.tasks}

    seen: set = set()
    ordered: List[TaskModel] = []
    for workflow in project.workflows:
        for step in sorted(workflow.steps, key=lambda s: s.step_order):
            task = task_by_iri.get(step.task_iri)
            if task and task.var_name not in seen:
                seen.add(task.var_name)
                ordered.append(task)

    remaining = [t for t in project.tasks if t.var_name not in seen]
    ordered.extend(remaining)

    return ordered or list(project.tasks)


def adapt(project: AgenticProject) -> AutoGenProject:
    """Map AgenticProject into AutoGenProject for the AutoGen generator."""
    project = project.model_copy(deep=True)
    # Ensure fallbacks are applied for Agent and Task values that may be missing in Core
    for agent in project.agents:
        if not agent.role:
            agent.role = "LLM Agent"
        if not agent.goal:
            agent.goal = agent.role
        if not agent.backstory and agent.system_prompt:
            agent.backstory = agent.system_prompt
        if not agent.system_prompt and agent.backstory:
            agent.system_prompt = agent.backstory
        if not agent.backstory:
            agent.backstory = f"You are a {agent.role}."
        if not agent.system_prompt:
            agent.system_prompt = agent.backstory

    for task in project.tasks:
        if not task.description and task.prompt_instruction:
            task.description = task.prompt_instruction
        if not task.description:
            task.description = task.var_name.replace("_", " ").title()
        if not task.expected_output:
            task.expected_output = f"Completed: {task.var_name}"

    return AutoGenProject(
        name=project.name,
        model_name=_resolve_model_name(project),
        agents=project.agents,
        tasks=list(project.tasks),
        workflows=project.workflows,
        tools=project.tools,
        ordered_tasks=_build_ordered_tasks(project),
        env_vars=project.env_vars,
        human_agents=project.human_agents,
        goals=project.goals,
        objectives=project.objectives,
        capabilities=project.capabilities,
        environments=project.environments,
        resources=project.resources,
        constraints=project.constraints,
    )
