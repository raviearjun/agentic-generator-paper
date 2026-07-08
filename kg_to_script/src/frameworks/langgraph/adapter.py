"""LangGraph adapter: maps AgenticProject → LangGraphProject."""

from __future__ import annotations

import re
from typing import Dict, List

from ...core.models import (
    AgenticProject,
)
from .models import (
    LangGraphAgentModel,
    LangGraphEdgeModel,
    LangGraphNodeModel,
    LangGraphProject,
    LangGraphRouteModel,
    LangGraphToolModel,
)


def _to_lower_camel(name: str) -> str:
    """Convert snake/kebab/space names to lowerCamelCase for TS identifiers."""
    if not name:
        return "node"
    parts = re.split(r"[^a-zA-Z0-9]+", name)
    parts = [p for p in parts if p]
    if not parts:
        return "node"
    out = parts[0].lower() + "".join(p[:1].upper() + p[1:] for p in parts[1:])
    if out[0].isdigit():
        out = f"n{out}"
    return out



def _map_tools(project: AgenticProject) -> List[LangGraphToolModel]:
    mapped: List[LangGraphToolModel] = []
    for tool in project.tools:
        # Derive a clean title from the label (class_name was removed from canonical ToolModel)
        title = re.sub(r"[^a-zA-Z0-9]", "", tool.label) if tool.label else tool.var_name
        mapped.append(
            LangGraphToolModel(
                iri=tool.iri,
                var_name=tool.var_name,
                title=title,
                description=tool.description or "A tool",
            )
        )
    return mapped


def _infer_model_name(lm_name: str, lm_desc: str) -> str:
    text = f"{lm_name} {lm_desc}".lower()
    # Try exact match first for common models
    for m_name in ["gpt-4o-mini", "gpt-4o", "gpt-4", "claude-3.5-sonnet", "claude-3.7-sonnet"]:
        if m_name in text:
            return m_name
    m = re.search(r"(gpt-[a-z0-9._-]+|claude-[a-z0-9._-]+)", text)
    if m:
        return m.group(1)
    return "gpt-4o-mini"


def _infer_provider(model_name: str) -> str:
    """Map a model identifier to its LangChain provider package."""
    name = model_name.lower()
    if "claude" in name:
        return "anthropic"
    return "openai"


def _map_agents(project: AgenticProject) -> List[LangGraphAgentModel]:
    mapped: List[LangGraphAgentModel] = []
    for agent in project.agents:
        lm = agent.language_model
        model_name = "gpt-4o-mini"
        if lm:
            model_name = lm.model_name or _infer_model_name(lm.name, lm.description)
        prompt = agent.system_prompt or agent.backstory
        if not prompt:
            prompt = f"You are a {agent.role}." if agent.role else "You are a helpful assistant."
        mapped.append(
            LangGraphAgentModel(
                iri=agent.iri,
                var_name=agent.var_name,
                role=agent.role or "agent",
                prompt=prompt,
                model_name=model_name,
                provider=_infer_provider(model_name),
                tools_refs=agent.tool_iris,
            )
        )
    return mapped


def _map_nodes_edges(project: AgenticProject) -> tuple[List[LangGraphNodeModel], List[LangGraphEdgeModel]]:
    step_by_iri: Dict[str, LangGraphNodeModel] = {}
    edges: List[LangGraphEdgeModel] = []
    task_by_iri: Dict[str, str] = {task.iri: task.description for task in project.tasks if task.iri}

    for workflow in project.workflows:
        for step in workflow.steps:
            if not step.iri:
                continue
            step_by_iri[step.iri] = LangGraphNodeModel(
                iri=step.iri,
                name=step.task_var_name or step.var_name or "step",
                ts_name=_to_lower_camel(step.task_var_name or step.var_name or "step"),
                agent_ref=step.agent_iri or None,
                node_kind="worker",
                group="nodes",
                is_start=step.step_type == "StartStep",
                is_end=step.step_type == "EndStep",
                task_description=task_by_iri.get(step.task_iri, ""),
            )
            for target in step.next_step_iris:
                edges.append(LangGraphEdgeModel(source=step.iri, target=target))

    if not step_by_iri:
        for idx, task in enumerate(project.tasks):
            step_iri = f"task-step:{task.iri}"
            step_by_iri[step_iri] = LangGraphNodeModel(
                iri=step_iri,
                name=task.var_name,
                ts_name=_to_lower_camel(task.var_name),
                agent_ref=task.agent_iri or None,
                node_kind="worker",
                group="nodes",
                is_start=idx == 0,
                is_end=idx == len(project.tasks) - 1,
                task_description=task.description,
            )
            if idx > 0:
                prev_iri = f"task-step:{project.tasks[idx - 1].iri}"
                edges.append(LangGraphEdgeModel(source=prev_iri, target=step_iri))

    has_outgoing = {edge.source for edge in edges}
    for node in step_by_iri.values():
        if node.iri not in has_outgoing and len(step_by_iri) > 0:
            node.is_end = True

    return list(step_by_iri.values()), edges


def _is_supervisor_topology(
    nodes: List[LangGraphNodeModel], edges: List[LangGraphEdgeModel]
) -> bool:
    """Return True only when the graph has an explicit hub-and-spoke supervisor topology.

    Criterion: there is a node explicitly named 'router' that has outgoing edges to
    more than one other node. Branching DAGs where a non-router node happens to have
    out-degree > 1 (like trip-planner's extraction step) are NOT supervisors.
    """
    return any(
        ("router" in n.name.lower() or "router" in n.ts_name.lower())
        and sum(1 for e in edges if e.source == n.iri) > 1
        for n in nodes
    )


def _resolve_router_and_routes(
    nodes: List[LangGraphNodeModel], edges: List[LangGraphEdgeModel]
) -> tuple[str, List[LangGraphRouteModel]]:
    """Infer supervisor router node and route table from graph topology.

    Only classifies the graph as supervisor when a node explicitly named 'router'
    has multiple outgoing edges. This avoids misclassifying branching DAGs.
    """
    by_iri = {n.iri: n for n in nodes}
    routes: List[LangGraphRouteModel] = []

    if not _is_supervisor_topology(nodes, edges):
        return "", routes

    # Locate the explicit router node
    named_router = next(
        (n for n in nodes if "router" in n.name.lower() or "router" in n.ts_name.lower()),
        None,
    )
    if not named_router:
        return "", routes

    router_iri = named_router.iri
    router_node = by_iri[router_iri]
    router_node.node_kind = "router"

    router_edges = [e for e in edges if e.source == router_iri]
    for edge in router_edges:
        target = by_iri.get(edge.target)
        if not target:
            continue
        route_key = target.ts_name
        fallback = "general" in target.ts_name.lower() or "chat" in target.ts_name.lower()
        if fallback:
            target.node_kind = "general_input"
        routes.append(
            LangGraphRouteModel(
                source_node=router_node.ts_name,
                target_node=target.ts_name,
                route_key=route_key,
                is_fallback=fallback,
            )
        )

    return router_node.ts_name, routes


def adapt(project: AgenticProject) -> LangGraphProject:
    """Adapt framework-agnostic AgenticProject into LangGraphProject."""
    project = project.model_copy(deep=True)
    # Ensure fallbacks are applied for Agent and Task values that may be missing in Core
    for agent in project.agents:
        if not agent.role:
            agent.role = "agent"
        if not agent.goal:
            agent.goal = agent.role

    for task in project.tasks:
        if not task.description and task.prompt_instruction:
            task.description = task.prompt_instruction
        if not task.description:
            task.description = task.var_name.replace("_", " ").title()
        if not task.expected_output:
            task.expected_output = f"Completed: {task.var_name}"

    tools = _map_tools(project)
    agents = _map_agents(project)
    nodes, edges = _map_nodes_edges(project)
    router_node_name, routes = _resolve_router_and_routes(nodes, edges)
    start_node_name = next((n.ts_name for n in nodes if n.is_start), "") or (nodes[0].ts_name if nodes else "")

    # Collect original KG workflow identifiers so they appear in generated code
    # for OEC matching. Both var_name and label are included as aliases.
    workflow_names: list = []
    for wf in project.workflows:
        if wf.var_name and wf.var_name not in workflow_names:
            workflow_names.append(wf.var_name)
        if wf.label and wf.label not in workflow_names:
            workflow_names.append(wf.label)

    return LangGraphProject(
        name=project.name or "LangGraph Project",
        tools=tools,
        agents=agents,
        nodes=nodes,
        edges=edges,
        routes=routes,
        router_node_name=router_node_name,
        start_node_name=start_node_name,
        workflow_names=workflow_names,
        tasks=list(project.tasks),
        human_agents=project.human_agents,
        goals=project.goals,
        objectives=project.objectives,
        capabilities=project.capabilities,
        environments=project.environments,
        resources=project.resources,
        constraints=project.constraints,
    )
