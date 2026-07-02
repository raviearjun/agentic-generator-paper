"""Extract evaluation elements and workflow graph from an AgentO KG."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

from src.core.extractor import extract_project

from ..config import IMPORTANT_CONFIG_KEYS
from ..schemas import EvaluationElement, ExtractionResult, GraphSpec
from ..utils import aliases_for, first_non_empty, local_name, normalize_name


def _element(category: str, name: str, *aliases: object, important: bool = False, **details: object) -> EvaluationElement:
    normalized_name = normalize_name(name)
    return EvaluationElement(
        category=category,
        name=normalized_name,
        aliases=aliases_for(name, *aliases),
        important=important,
        details=tuple(sorted((key, str(value)) for key, value in details.items() if value not in (None, ""))),
    )


def _config_element(owner_category: str, owner_name: str, key: str, value: str) -> EvaluationElement:
    normalized_key = normalize_name(key)
    normalized_owner = normalize_name(owner_name)
    return _element(
        "config",
        f"{owner_category}:{normalized_owner}:{normalized_key}",
        key,
        value,
        f"{key}_{value}",
        important=normalized_key in IMPORTANT_CONFIG_KEYS,
        owner_category=owner_category,
        owner=normalized_owner,
        key=normalized_key,
        value=value,
    )


def _relation(category: str, source: str, target: str, *aliases: object, important: bool = False) -> EvaluationElement:
    source_name = normalize_name(source)
    target_name = normalize_name(target)
    return _element(
        category,
        f"{source_name}->{target_name}",
        source,
        target,
        *aliases,
        important=important,
        source=source_name,
        target=target_name,
    )


def extract_kg(kg_path: Path) -> ExtractionResult:
    project = extract_project(str(kg_path))
    elements: List[EvaluationElement] = []

    agent_by_iri = {agent.iri: agent for agent in project.agents}
    task_by_iri = {task.iri: task for task in project.tasks}
    tool_by_iri = {tool.iri: tool for tool in project.tools}

    elements.append(_element("project", project.var_name or project.name, project.name, important=False))

    for key, value in project.system_configs.items():
        elements.append(_config_element("system", project.var_name or project.name, key, value))

    for env_var in project.env_vars:
        elements.append(_config_element("env", project.var_name or project.name, env_var.key, env_var.value))

    for agent in project.agents:
        elements.append(_element("agent", agent.var_name, agent.agent_id, agent.role, local_name(agent.iri), important=True))
        if agent.goal_iri:
            elements.append(_relation("agent_goal", agent.var_name, local_name(agent.goal_iri), important=False))
        if agent.language_model:
            elements.append(_relation("agent_llm", agent.var_name, agent.language_model.name or local_name(agent.language_model.iri), important=False))
        for key, value in agent.configs.items():
            elements.append(_config_element("agent", agent.var_name, key, value))
        for tool_iri in agent.tool_iris:
            tool = tool_by_iri.get(tool_iri)
            target = tool.var_name if tool else local_name(tool_iri)
            elements.append(_relation("agent_tool", agent.var_name, target, important=True))
        for target_iri in agent.interacts_with:
            target = agent_by_iri.get(target_iri)
            elements.append(_relation("agent_interaction", agent.var_name, target.var_name if target else local_name(target_iri), important=True))
        for cap_iri in agent.capability_iris:
            elements.append(_relation("agent_capability", agent.var_name, local_name(cap_iri), important=False))

    for task in project.tasks:
        display = first_non_empty([task.var_name, task.label, local_name(task.iri)])
        elements.append(_element("task", display, task.label, local_name(task.iri), important=True))
        agent_name = task.agent_var_name or (agent_by_iri.get(task.agent_iri).var_name if task.agent_iri in agent_by_iri else "")
        if agent_name:
            elements.append(_relation("task_agent", display, agent_name, important=True))
        for key, value in task.configs.items():
            elements.append(_config_element("task", display, key, value))
        for resource_iri in task.produced_resources:
            elements.append(_relation("task_produces", display, local_name(resource_iri), important=False))
        for resource_iri in task.required_resources:
            elements.append(_relation("task_requires", display, local_name(resource_iri), important=False))
        for cap_iri in task.requires_capability_iris:
            elements.append(_relation("task_capability", display, local_name(cap_iri), important=False))
        for context_task in task.context_task_var_names:
            elements.append(_relation("task_context", display, context_task, important=True))

    for tool in project.tools:
        elements.append(_element("tool", tool.var_name, tool.label, local_name(tool.iri), important=True))
        for config in tool.configs:
            elements.append(_config_element("tool", tool.var_name, config.key, config.value))
        for cap_iri in tool.capability_iris:
            elements.append(_relation("tool_capability", tool.var_name, local_name(cap_iri), important=False))

    for workflow in project.workflows:
        workflow_name = workflow.var_name or workflow.label or local_name(workflow.iri)
        elements.append(_element("workflow", workflow_name, workflow.label, local_name(workflow.iri), important=True))
        for step in workflow.steps:
            step_name = _step_name(step, task_by_iri)
            elements.append(_element("workflow_step", step_name, step.var_name, local_name(step.iri), important=True))
            if step.task_var_name:
                elements.append(_relation("step_task", step_name, step.task_var_name, important=True))

    for collection, category in [
        (project.memories, "memory"),
        (project.language_models, "language_model"),
        (project.goals, "goal"),
        (project.capabilities, "capability"),
        (project.environments, "environment"),
        (project.objectives, "objective"),
        (project.human_agents, "human_agent"),
        (project.resources, "resource"),
        (project.constraints, "constraint"),
    ]:
        for item in collection:
            item_name = first_non_empty([getattr(item, "var_name", ""), getattr(item, "name", ""), getattr(item, "label", ""), local_name(getattr(item, "iri", ""))])
            elements.append(_element(category, item_name, getattr(item, "label", ""), local_name(getattr(item, "iri", "")), important=False))

    graph = _workflow_graph(project.workflows, task_by_iri)
    return ExtractionResult(
        elements=_dedupe_elements(elements),
        graph=graph,
        metadata={"project": project.name, "kg_path": str(kg_path)},
    )


def _step_name(step, task_by_iri: Dict[str, object]) -> str:
    if step.task_var_name:
        return step.task_var_name
    if step.task_iri in task_by_iri:
        return task_by_iri[step.task_iri].var_name
    return step.var_name or local_name(step.iri)


def _workflow_graph(workflows: Iterable[object], task_by_iri: Dict[str, object]) -> GraphSpec:
    graph = GraphSpec()
    for workflow in workflows:
        step_by_iri = {step.iri: step for step in workflow.steps if step.iri}
        ordered_steps = sorted(workflow.steps, key=lambda item: (item.step_order, _step_name(item, task_by_iri)))

        # Collect explicit :nextStep edges for THIS workflow only.
        wf_edges: set = set()
        for step in ordered_steps:
            node = normalize_name(_step_name(step, task_by_iri))
            graph.nodes.add(node)
            for next_iri in step.next_step_iris:
                next_step = step_by_iri.get(next_iri)
                if next_step:
                    target = normalize_name(_step_name(next_step, task_by_iri))
                    wf_edges.add((node, target))

        # Apply sequential fallback only when THIS workflow has no explicit edges.
        if not wf_edges and len(ordered_steps) > 1:
            for source, target in zip(ordered_steps, ordered_steps[1:]):
                wf_edges.add((normalize_name(_step_name(source, task_by_iri)), normalize_name(_step_name(target, task_by_iri))))

        graph.edges.update(wf_edges)

    return graph



def _dedupe_elements(elements: List[EvaluationElement]) -> List[EvaluationElement]:
    seen = set()
    unique = []
    for element in elements:
        if not element.name:
            continue
        key = (element.category, element.name)
        if key in seen:
            continue
        seen.add(key)
        unique.append(element)
    return unique
