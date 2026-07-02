"""agentO extraction pipeline: KG (.ttl) → AgenticProject IR.

This module is the single entry point for KG extraction. It:
  1. Loads a Turtle graph via rdflib.
  2. Runs SPARQL queries (defined in queries.py) against the graph.
  3. Maps results into canonical IR models (defined in models.py).
  4. Returns a fully populated AgenticProject.

Nothing here is framework-specific. All framework conveniences belong in
the respective adapter layer (crewai/adapter.py, autogen/adapter.py, etc.).
"""

from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional, Set, Tuple

from rdflib import Graph

from .helpers import camel, extract_placeholders, load_graph, s, safe_var
from .models import (
    AgenticProject,
    AgentModel,
    CapabilityModel,
    ConfigModel,
    ConstraintModel,
    EnvironmentModel,
    GoalModel,
    HumanAgentModel,
    LanguageModelModel,
    MemoryModel,
    ObjectiveModel,
    ResourceModel,
    TaskModel,
    ToolConfigModel,
    ToolModel,
    WorkflowPatternModel,
    WorkflowStepModel,
    WorkflowType,
)
from .queries import (
    AGENT_ALL_CONFIGS_QUERY,
    AGENT_CAPABILITY_QUERY,
    AGENT_INTERACTS_QUERY,
    AGENT_KNOWLEDGE_QUERY,
    AGENT_LLM_QUERY,
    AGENT_OBJECTIVE_QUERY,
    AGENT_OPERATES_IN_QUERY,
    AGENT_TOOLS_QUERY,
    AGENTS_QUERY,
    CAPABILITIES_QUERY,
    CONSTRAINT_CONFIGS_QUERY,
    CONSTRAINTS_QUERY,
    ENV_CONFIG_QUERY,
    ENVIRONMENT_CONFIGS_QUERY,
    ENVIRONMENT_CONTAINS_QUERY,
    ENVIRONMENTS_QUERY,
    GOALS_QUERY,
    HUMAN_AGENTS_QUERY,
    HUMAN_PARTICIPATED_QUERY,
    LLM_QUERY,
    MEMORY_CONFIG_QUERY,
    MEMORY_QUERY,
    OBJECTIVES_QUERY,
    RESOURCES_QUERY,
    STEP_EDGES_QUERY,
    SYSTEM_CONFIG_QUERY,
    TASK_CAPABILITY_QUERY,
    TASK_CONFIG_QUERY,
    TASK_OBJECTIVE_QUERY,
    TASK_PERFORMED_BY_QUERY,
    TASK_PRODUCES_QUERY,
    TASK_PROMPT_QUERY,
    TASK_REQUIRES_QUERY,
    TASKS_QUERY,
    TEAM_AGENT_MEMBERS_QUERY,
    TEAM_GOAL_QUERY,
    TEAM_OBJECTIVE_QUERY,
    TEAM_QUERY,
    TEAM_TEAM_GOAL_QUERY,
    TEAM_WORKFLOW_PATTERN_QUERY,
    TOOL_CAPABILITY_QUERY,
    TOOL_CONFIGS_QUERY,
    TOOL_RESOURCE_USAGE_QUERY,
    TOOL_TOOL_USAGE_QUERY,
    TOOLS_QUERY,
    WORKFLOW_NEXT_PATTERN_QUERY,
    WORKFLOW_PATTERN_QUERY,
    WORKFLOW_QUERY,
    WORKFLOW_RELATED_PATTERN_QUERY,
    WORKFLOW_STEPS_QUERY,
    WORKFLOW_SUB_PATTERN_QUERY,
)

logger = logging.getLogger(__name__)

# Orchestration configuration keys and values derived from standard AgentO conventions.
ORCHESTRATION_CONFIG_KEY = "process"
ORCHESTRATION_SEQUENTIAL = "sequential"
ORCHESTRATION_HIERARCHICAL = "hierarchical"


# ─────────────────────── Internal helpers ───────────────────────
def _has_cycle(steps: List[WorkflowStepModel], edges: List[Tuple[str, str]]) -> bool:
    """Return True if the directed step graph contains any cycle (DFS)."""
    adjacency: Dict[str, List[str]] = {}
    for src, tgt in edges:
        adjacency.setdefault(src, []).append(tgt)

    visited: Set[str] = set()
    rec_stack: Set[str] = set()

    def dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbour in adjacency.get(node, []):
            if neighbour not in visited:
                if dfs(neighbour):
                    return True
            elif neighbour in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    return any(dfs(step.iri) for step in steps if step.iri and step.iri not in visited)


# ─────────────────────── Extraction functions ───────────────────────

def _extract_team(g: Graph, system_configs: Dict[str, str]) -> Tuple[str, str, str, str]:
    """Extract team/project name, description, orchestration-mode keyword, and team IRI.

    Returns:
        (project_name, description, orchestration_mode, team_iri)

    orchestration_mode is a raw string ('sequential', 'hierarchical', or '')
    that adapters can interpret in framework-specific terms.
    """
    project_name = "UnnamedProject"
    description = ""
    orchestration_mode = ""
    team_iri = ""

    results = list(g.query(TEAM_QUERY))
    if results:
        row = results[0]
        team_iri = s(row.team)
        label = s(row.label)
        if label:
            project_name = re.sub(r"[^a-zA-Z0-9]", "", label) or "UnnamedProject"
        else:
            # Fallback: extract local name from team IRI (e.g., "#JobPostingCrew" → "JobPostingCrew")
            local_name = team_iri.split("/")[-1].split("#")[-1]
            if local_name:
                project_name = re.sub(r"[^a-zA-Z0-9]", "", local_name) or "UnnamedProject"
        description = s(row.desc)

    process_value = system_configs.get(ORCHESTRATION_CONFIG_KEY, "").strip().lower()
    if ORCHESTRATION_HIERARCHICAL in process_value:
        orchestration_mode = ORCHESTRATION_HIERARCHICAL
    elif ORCHESTRATION_SEQUENTIAL in process_value:
        orchestration_mode = ORCHESTRATION_SEQUENTIAL

    return project_name, description, orchestration_mode, team_iri


def _extract_language_models(g: Graph) -> Dict[str, LanguageModelModel]:
    """Extract :LanguageModel individuals keyed by IRI.

    Only data explicitly asserted in the KG is stored. Provider/model_name
    inference from free text is left to adapters that know their framework's
    LLM initialization requirements.
    """
    models: Dict[str, LanguageModelModel] = {}
    for row in g.query(LLM_QUERY):
        iri = s(row.lm)
        label = s(row.label)
        desc = s(row.desc)
        models[iri] = LanguageModelModel(
            iri=iri,
            name=label,
            description=desc,
            # provider and model_name start empty; adapters may populate them
            # by inspecting name/description if needed for their framework
        )
    return models


def _extract_tools(g: Graph) -> Dict[str, ToolModel]:
    """Extract standalone :Tool individuals (excluding :LLMAgent subclasses)."""
    tools: Dict[str, ToolModel] = {}

    for row in g.query(TOOLS_QUERY):
        iri = s(row.tool)
        if iri in tools:
            continue
        label = s(row.label)
        desc = s(row.desc) or s(row.comment) or ""

        tools[iri] = ToolModel(
            iri=iri,
            var_name=safe_var(iri),
            label=label,
            description=desc.strip(),
            configs=[],
            capability_iris=[],
            resource_usage_iris=[],
            tool_usage_iris=[],
        )

    for row in g.query(TOOL_CONFIGS_QUERY):
        iri = s(row.tool)
        if iri in tools:
            tools[iri].configs.append(
                ToolConfigModel(key=s(row.key), value=s(row.value))
            )

    return tools


def _extract_agents(
    g: Graph,
    tools_map: Dict[str, ToolModel],
    lm_map: Dict[str, LanguageModelModel],
) -> Dict[str, AgentModel]:
    """Extract :LLMAgent individuals from the KG.

    Single consolidated SPARQL query extracts all scalar properties.
    Multi-valued relations (tools, LLM, knowledge) use separate queries.
    Framework-specific derived fields (allow_delegation, verbose, tool_var_names)
    are NOT computed here — adapters derive them from the raw configs dict.
    """
    agents: Dict[str, AgentModel] = {}

    for row in g.query(AGENTS_QUERY):
        iri = s(row.agent)
        if iri in agents:
            continue

        agent_id = s(row.agentID)
        label = s(row.label)
        role = s(row.role)

        var_name = agent_id or label or safe_var(iri)
        var_name = safe_var(var_name) if not re.match(r'^[a-z_][a-z0-9_]*$', var_name) else var_name

        prompt_context = s(row.backstory)

        agents[iri] = AgentModel(
            iri=iri,
            var_name=var_name,
            agent_id=agent_id,
            role=role,
            goal=s(row.goalDesc),
            goal_iri=s(row.goal),
            backstory=prompt_context,
            system_prompt=prompt_context,
            tool_iris=[],
            language_model=None,
            knowledge_iris=[],
            configs={},
        )

    # Raw configs — adapters read framework-specific keys (allow_delegation, verbose, etc.)
    for row in g.query(AGENT_ALL_CONFIGS_QUERY):
        iri = s(row.agent)
        if iri in agents:
            agents[iri].configs[s(row.key)] = s(row.value)

    # Agent → Tool links
    for row in g.query(AGENT_TOOLS_QUERY):
        iri = s(row.agent)
        tool_iri = s(row.tool)
        if iri in agents and tool_iri in tools_map:
            if tool_iri not in agents[iri].tool_iris:
                agents[iri].tool_iris.append(tool_iri)

    # Agent → LanguageModel
    for row in g.query(AGENT_LLM_QUERY):
        iri = s(row.agent)
        lm_iri = s(row.lm)
        if iri in agents and lm_iri in lm_map:
            agents[iri].language_model = lm_map[lm_iri]

    # Agent → Knowledge
    for row in g.query(AGENT_KNOWLEDGE_QUERY):
        iri = s(row.agent)
        knowledge_iri = s(row.knowledge)
        if iri in agents and knowledge_iri not in agents[iri].knowledge_iris:
            agents[iri].knowledge_iris.append(knowledge_iri)

    # Apply defaults for required fields that may be absent in the KG
    for agent in agents.values():
        if not agent.role:
            agent.role = "LLM Agent"

    return agents


def _extract_tasks(g: Graph, agents_map: Dict[str, AgentModel]) -> Dict[str, TaskModel]:
    """Extract :Task individuals with full property resolution."""
    tasks: Dict[str, TaskModel] = {}

    agent_iri_to_var: Dict[str, str] = {a.iri: a.var_name for a in agents_map.values()}

    for row in g.query(TASKS_QUERY):
        iri = s(row.task)
        if iri in tasks:
            continue

        label = s(row.label)
        desc = s(row.desc)
        agent_iri = s(row.agent)

        var_name = label or safe_var(iri)
        var_name = safe_var(var_name) if not re.match(r'^[a-z_][a-z0-9_]*$', var_name) else var_name

        tasks[iri] = TaskModel(
            iri=iri,
            var_name=var_name,
            label=label,
            description=desc,
            expected_output="",
            agent_iri=agent_iri,
            agent_var_name=agent_iri_to_var.get(agent_iri, ""),
            context_task_var_names=[],
            produced_resources=[],
            required_resources=[],
            configs={},
        )

    for row in g.query(TASK_CONFIG_QUERY):
        iri = s(row.task)
        if iri in tasks:
            tasks[iri].configs[s(row.key)] = s(row.value)

    # Extract description and expected_output from task config bag if available
    for task in tasks.values():
        cfg_desc = task.configs.get("description", "")
        if cfg_desc and len(cfg_desc) > len(task.description):
            task.description = cfg_desc

    # Prompt data
    for row in g.query(TASK_PROMPT_QUERY):
        iri = s(row.task)
        if iri not in tasks:
            continue
        instr = s(row.instruction)
        input_data = s(row.inputData)
        output = s(row.outputIndicator)
        context = s(row.context)
        tasks[iri].prompt_instruction = instr
        tasks[iri].prompt_input_data = input_data
        tasks[iri].prompt_output_indicator = output
        tasks[iri].prompt_context = context
        if output and not tasks[iri].expected_output:
            tasks[iri].expected_output = output
        if instr and not tasks[iri].description:
            tasks[iri].description = instr

    # Expected output from Config if not set by prompt indicator
    for task in tasks.values():
        cfg_eo = task.configs.get("expected_output", "")
        if cfg_eo and not task.expected_output:
            task.expected_output = cfg_eo

    return tasks


def _resolve_task_context(g: Graph, tasks_map: Dict[str, TaskModel]) -> None:
    """Resolve task dependency chains via producedResource / requiresResource.

    If Task B requiresResource R, and Task A producedResource R,
    then Task B's context_task_var_names includes Task A's var_name.
    """
    resource_to_producer: Dict[str, str] = {}
    for row in g.query(TASK_PRODUCES_QUERY):
        task_iri = s(row.task)
        res_iri = s(row.resource)
        if task_iri in tasks_map:
            if res_iri not in tasks_map[task_iri].produced_resources:
                tasks_map[task_iri].produced_resources.append(res_iri)
            resource_to_producer[res_iri] = tasks_map[task_iri].var_name

    for row in g.query(TASK_REQUIRES_QUERY):
        task_iri = s(row.task)
        res_iri = s(row.resource)
        if task_iri in tasks_map:
            task = tasks_map[task_iri]
            if res_iri not in task.required_resources:
                task.required_resources.append(res_iri)
            if res_iri in resource_to_producer:
                producer_var = resource_to_producer[res_iri]
                if producer_var != task.var_name and producer_var not in task.context_task_var_names:
                    task.context_task_var_names.append(producer_var)


def _extract_workflow(g: Graph, tasks_map: Dict[str, TaskModel]) -> List[WorkflowStepModel]:
    """Extract :WorkflowStep individuals in step order."""
    steps: List[WorkflowStepModel] = []
    task_iri_to_var: Dict[str, str] = {t.iri: t.var_name for t in tasks_map.values()}
    task_iri_to_agent: Dict[str, str] = {t.iri: t.agent_iri for t in tasks_map.values()}

    edge_map: Dict[str, List[str]] = {}
    for row in g.query(STEP_EDGES_QUERY):
        source = s(row.source)
        target = s(row.target)
        edge_map.setdefault(source, [])
        if target not in edge_map[source]:
            edge_map[source].append(target)

    for row in g.query(WORKFLOW_QUERY):
        step_iri = s(row.step)
        task_iri = s(row.task)
        task_var = task_iri_to_var.get(task_iri, safe_var(task_iri))
        order = int(row.stepOrder) if row.stepOrder is not None else len(steps) + 1
        step_type = s(row.stepType).split("#")[-1] if row.stepType else "WorkflowStep"

        steps.append(WorkflowStepModel(
            iri=step_iri,
            var_name=safe_var(step_iri),
            step_order=order,
            task_iri=task_iri,
            task_var_name=task_var,
            step_type=step_type,
            next_step_iris=edge_map.get(step_iri, []),
            agent_iri=task_iri_to_agent.get(task_iri, ""),
        ))

    steps.sort(key=lambda step: step.step_order)
    return steps


def _infer_workflow_type(orchestration_mode: str, steps: List[WorkflowStepModel]) -> WorkflowType:
    """Infer a framework-agnostic workflow topology from step edge structure.

    Uses DFS-based cycle detection for accurate LOOP classification.
    """
    if orchestration_mode == "hierarchical":
        return WorkflowType.HIERARCHICAL
    if not steps:
        return WorkflowType.SEQUENTIAL

    edges = [(step.iri, target) for step in steps for target in step.next_step_iris]

    if _has_cycle(steps, edges):
        return WorkflowType.LOOP
    if any(len(step.next_step_iris) > 1 for step in steps):
        return WorkflowType.BRANCHING
    if len(edges) == 0 and len(steps) > 1:
        return WorkflowType.PARALLEL
    return WorkflowType.SEQUENTIAL


def _extract_memories(g: Graph) -> Dict[str, MemoryModel]:
    """Extract :Memory individuals and raw configs."""
    memories: Dict[str, MemoryModel] = {}
    for row in g.query(MEMORY_QUERY):
        iri = s(row.mem)
        if iri not in memories:
            memories[iri] = MemoryModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc),
                configs={},
            )

    for row in g.query(MEMORY_CONFIG_QUERY):
        iri = s(row.mem)
        if iri in memories:
            memories[iri].configs[s(row.key)] = s(row.value)
    return memories


def _extract_workflow_patterns(
    g: Graph,
    steps: List[WorkflowStepModel],
    orchestration_mode: str,
) -> List[WorkflowPatternModel]:
    """Extract :WorkflowPattern containers and attach :WorkflowStep members."""
    patterns: Dict[str, WorkflowPatternModel] = {}
    step_by_iri = {step.iri: step for step in steps if step.iri}
    inferred_type = _infer_workflow_type(orchestration_mode, steps)

    for row in g.query(WORKFLOW_PATTERN_QUERY):
        iri = s(row.wp)
        patterns[iri] = WorkflowPatternModel(
            iri=iri,
            var_name=safe_var(iri),
            label=s(row.label),
            description=s(row.desc),
            steps=[],
            workflow_type=inferred_type,
            sub_pattern_iris=[],
        )

    for row in g.query(WORKFLOW_STEPS_QUERY):
        wp_iri = s(row.wp)
        step_iri = s(row.step)
        if wp_iri in patterns and step_iri in step_by_iri:
            patterns[wp_iri].steps.append(step_by_iri[step_iri])

    for row in g.query(WORKFLOW_SUB_PATTERN_QUERY):
        wp_iri = s(row.wp)
        sub_iri = s(row.sub)
        if wp_iri in patterns and sub_iri not in patterns[wp_iri].sub_pattern_iris:
            patterns[wp_iri].sub_pattern_iris.append(sub_iri)

    # Fallback: if no pattern exists but steps do, create a synthetic default
    if not patterns and steps:
        patterns["default-workflow"] = WorkflowPatternModel(
            iri="default-workflow",
            var_name="default_workflow",
            label="Default Workflow",
            steps=steps,
            workflow_type=inferred_type,
        )

    for pattern in patterns.values():
        pattern.steps.sort(key=lambda step: step.step_order)
    return list(patterns.values())


def _extract_system_configs(g: Graph) -> Dict[str, str]:
    """Extract :Team-level system configs as raw key/value strings."""
    configs: Dict[str, str] = {}
    for row in g.query(SYSTEM_CONFIG_QUERY):
        configs[s(row.key)] = s(row.value)
    return configs


def _extract_env_vars(g: Graph) -> List[ConfigModel]:
    """Extract environment variable configs (API keys, etc.)."""
    env_vars: List[ConfigModel] = []
    seen: Set[str] = set()
    for row in g.query(ENV_CONFIG_QUERY):
        key = s(row.key)
        if key not in seen:
            seen.add(key)
            env_vars.append(ConfigModel(key=key, value=s(row.value)))
    return env_vars


def _extract_goals(g: Graph) -> Dict[str, GoalModel]:
    """Extract all :Goal individuals keyed by IRI."""
    goals: Dict[str, GoalModel] = {}
    for row in g.query(GOALS_QUERY):
        iri = s(row.goal)
        if iri not in goals:
            goals[iri] = GoalModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc),
            )
    return goals


def _extract_capabilities(g: Graph) -> Dict[str, CapabilityModel]:
    """Extract all :Capability individuals keyed by IRI."""
    caps: Dict[str, CapabilityModel] = {}
    for row in g.query(CAPABILITIES_QUERY):
        iri = s(row.cap)
        if iri not in caps:
            caps[iri] = CapabilityModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc) or s(row.comment) or "",
            )
    return caps


def _extract_environments(g: Graph) -> Dict[str, EnvironmentModel]:
    """Extract all :Environment individuals keyed by IRI."""
    envs: Dict[str, EnvironmentModel] = {}
    for row in g.query(ENVIRONMENTS_QUERY):
        iri = s(row.env)
        if iri not in envs:
            envs[iri] = EnvironmentModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc),
                env_type=s(row.envType),
            )

    for row in g.query(ENVIRONMENT_CONFIGS_QUERY):
        iri = s(row.env)
        if iri in envs:
            envs[iri].configs[s(row.key)] = s(row.value)

    for row in g.query(ENVIRONMENT_CONTAINS_QUERY):
        iri = s(row.env)
        res_iri = s(row.resource)
        if iri in envs and res_iri not in envs[iri].contained_resource_iris:
            envs[iri].contained_resource_iris.append(res_iri)

    return envs


def _extract_objectives(g: Graph) -> Dict[str, ObjectiveModel]:
    """Extract all :Objective individuals keyed by IRI."""
    objs: Dict[str, ObjectiveModel] = {}
    for row in g.query(OBJECTIVES_QUERY):
        iri = s(row.obj)
        if iri not in objs:
            objs[iri] = ObjectiveModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc),
                contributes_to_goal_iri=s(row.goal),
            )
    return objs


def _extract_human_agents(g: Graph) -> Dict[str, HumanAgentModel]:
    """Extract all :HumanAgent individuals keyed by IRI."""
    humans: Dict[str, HumanAgentModel] = {}
    for row in g.query(HUMAN_AGENTS_QUERY):
        iri = s(row.human)
        if iri not in humans:
            humans[iri] = HumanAgentModel(
                iri=iri,
                var_name=safe_var(iri),
                role=s(row.role),
            )

    for row in g.query(HUMAN_PARTICIPATED_QUERY):
        iri = s(row.human)
        task_iri = s(row.task)
        if iri in humans and task_iri not in humans[iri].participated_task_iris:
            humans[iri].participated_task_iris.append(task_iri)

    return humans


def _extract_resources(g: Graph) -> Dict[str, ResourceModel]:
    """Extract all beam:Resource (and beam:Instance) individuals keyed by IRI."""
    resources: Dict[str, ResourceModel] = {}
    for row in g.query(RESOURCES_QUERY):
        iri = s(row.res)
        if iri not in resources:
            type_frag = s(row.type).split("#")[-1].split("/")[-1]
            resources[iri] = ResourceModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc),
                resource_type=type_frag,
            )
    return resources


def _extract_constraints(g: Graph) -> Dict[str, ConstraintModel]:
    """Extract all :Constraint individuals keyed by IRI."""
    constraints: Dict[str, ConstraintModel] = {}
    for row in g.query(CONSTRAINTS_QUERY):
        iri = s(row.con)
        if iri not in constraints:
            constraints[iri] = ConstraintModel(
                iri=iri,
                var_name=safe_var(iri),
                label=s(row.label),
                description=s(row.desc),
            )

    for row in g.query(CONSTRAINT_CONFIGS_QUERY):
        iri = s(row.con)
        if iri in constraints:
            constraints[iri].configs[s(row.key)] = s(row.value)

    return constraints


# ── Cross-ontology linking ──

def _link_agent_relations(
    g: Graph,
    agents_map: Dict[str, AgentModel],
    tools_map: Dict[str, ToolModel],
    capabilities_map: Dict[str, CapabilityModel],
) -> None:
    """Populate agent → relationship fields (interactsWith, operatesIn, capabilities, objectives)."""
    for row in g.query(AGENT_INTERACTS_QUERY):
        iri = s(row.agent)
        target = s(row.target)
        if iri in agents_map and target not in agents_map[iri].interacts_with:
            agents_map[iri].interacts_with.append(target)

    for row in g.query(AGENT_OPERATES_IN_QUERY):
        iri = s(row.agent)
        env_iri = s(row.env)
        if iri in agents_map:
            agents_map[iri].operates_in_iri = env_iri

    for row in g.query(AGENT_CAPABILITY_QUERY):
        iri = s(row.agent)
        cap_iri = s(row.cap)
        if iri in agents_map and cap_iri not in agents_map[iri].capability_iris:
            agents_map[iri].capability_iris.append(cap_iri)

    for row in g.query(AGENT_OBJECTIVE_QUERY):
        iri = s(row.agent)
        obj_iri = s(row.obj)
        if iri in agents_map and obj_iri not in agents_map[iri].objective_iris:
            agents_map[iri].objective_iris.append(obj_iri)


def _link_task_relations(
    g: Graph,
    tasks_map: Dict[str, TaskModel],
) -> None:
    """Populate task → ontology relationship fields."""
    for row in g.query(TASK_OBJECTIVE_QUERY):
        iri = s(row.task)
        obj_iri = s(row.obj)
        if iri in tasks_map:
            tasks_map[iri].contributes_to_objective_iri = obj_iri

    for row in g.query(TASK_CAPABILITY_QUERY):
        iri = s(row.task)
        cap_iri = s(row.cap)
        if iri in tasks_map and cap_iri not in tasks_map[iri].requires_capability_iris:
            tasks_map[iri].requires_capability_iris.append(cap_iri)

    for row in g.query(TASK_PERFORMED_BY_QUERY):
        iri = s(row.task)
        performer = s(row.performer)
        if iri in tasks_map:
            tasks_map[iri].performed_by_iri = performer


def _link_tool_relations(
    g: Graph,
    tools_map: Dict[str, ToolModel],
    capabilities_map: Dict[str, CapabilityModel],
) -> None:
    """Populate tool → ontology relationship fields."""
    for row in g.query(TOOL_CAPABILITY_QUERY):
        iri = s(row.tool)
        cap_iri = s(row.cap)
        if iri in tools_map and cap_iri not in tools_map[iri].capability_iris:
            tools_map[iri].capability_iris.append(cap_iri)

    for row in g.query(TOOL_RESOURCE_USAGE_QUERY):
        iri = s(row.tool)
        res_iri = s(row.resource)
        if iri in tools_map and res_iri not in tools_map[iri].resource_usage_iris:
            tools_map[iri].resource_usage_iris.append(res_iri)

    for row in g.query(TOOL_TOOL_USAGE_QUERY):
        iri = s(row.tool)
        child_iri = s(row.child)
        if iri in tools_map and child_iri not in tools_map[iri].tool_usage_iris:
            tools_map[iri].tool_usage_iris.append(child_iri)


def _link_team_relations(
    g: Graph,
    project: AgenticProject,
    team_iri: str,
) -> None:
    """Populate team → ontology relationship fields on the project."""
    if not team_iri:
        return

    for row in g.query(TEAM_AGENT_MEMBERS_QUERY):
        iri = s(row.team)
        agent_iri = s(row.agent)
        if iri == team_iri and agent_iri not in project.agent_member_iris:
            project.agent_member_iris.append(agent_iri)

    for row in g.query(TEAM_WORKFLOW_PATTERN_QUERY):
        iri = s(row.team)
        wp_iri = s(row.wp)
        if iri == team_iri and wp_iri not in project.workflow_pattern_iris:
            project.workflow_pattern_iris.append(wp_iri)

    for row in g.query(TEAM_GOAL_QUERY):
        iri = s(row.team)
        goal_iri = s(row.goal)
        if iri == team_iri and goal_iri not in project.goal_iris:
            project.goal_iris.append(goal_iri)

    for row in g.query(TEAM_TEAM_GOAL_QUERY):
        iri = s(row.team)
        goal_iri = s(row.goal)
        if iri == team_iri and goal_iri not in project.goal_iris:
            project.goal_iris.append(goal_iri)

    for row in g.query(TEAM_OBJECTIVE_QUERY):
        iri = s(row.team)
        obj_iri = s(row.obj)
        if iri == team_iri and obj_iri not in project.objective_iris:
            project.objective_iris.append(obj_iri)


def _link_workflow_relations(
    g: Graph,
    patterns: List[WorkflowPatternModel],
) -> None:
    """Populate workflow pattern → pattern relationship fields."""
    pattern_by_iri = {p.iri: p for p in patterns if p.iri}

    for row in g.query(WORKFLOW_RELATED_PATTERN_QUERY):
        wp_iri = s(row.wp)
        rel_iri = s(row.related)
        if wp_iri in pattern_by_iri and rel_iri not in pattern_by_iri[wp_iri].related_pattern_iris:
            pattern_by_iri[wp_iri].related_pattern_iris.append(rel_iri)

    for row in g.query(WORKFLOW_NEXT_PATTERN_QUERY):
        wp_iri = s(row.wp)
        next_iri = s(row.next)
        if wp_iri in pattern_by_iri:
            pattern_by_iri[wp_iri].next_pattern_iri = next_iri


def _apply_human_input_flags(
    tasks_map: Dict[str, TaskModel],
    human_agents_map: Dict[str, HumanAgentModel],
) -> None:
    """Set task.human_input = True for any task a :HumanAgent participates in.

    Computed once here so all adapters see a consistent value without each
    independently re-deriving it from HumanAgent.participated_task_iris.
    """
    participated: Set[str] = set()
    for ha in human_agents_map.values():
        participated.update(ha.participated_task_iris)

    for task in tasks_map.values():
        if task.iri in participated:
            task.human_input = True


# ─────────────────────── Public API ───────────────────────

def extract_project(file_path: str) -> AgenticProject:
    """Parse a KG (.ttl) file and return a framework-agnostic AgenticProject.

    Pipeline:
        load_graph → SPARQL extraction → canonical IR → relationship linking

    The returned AgenticProject is ready for consumption by any framework adapter.
    Adapters are responsible for deriving all framework-specific fields
    (e.g. CrewAI allow_delegation, AutoGen model_name defaults, LangGraph node names).

    The orchestration mode ('sequential' / 'hierarchical' / '') is stored in
    system_configs["process"] for adapters that need it.
    """
    g = load_graph(file_path)

    system_configs = _extract_system_configs(g)
    project_name, description, orchestration_mode, team_iri = _extract_team(g, system_configs)
    project_var_name = safe_var(project_name)

    lm_map = _extract_language_models(g)
    tools_map = _extract_tools(g)
    memories_map = _extract_memories(g)
    agents_map = _extract_agents(g, tools_map, lm_map)
    tasks_map = _extract_tasks(g, agents_map)
    _resolve_task_context(g, tasks_map)
    workflow_steps = _extract_workflow(g, tasks_map)
    workflows = _extract_workflow_patterns(g, workflow_steps, orchestration_mode)

    # Full ontology coverage
    goals_map = _extract_goals(g)
    capabilities_map = _extract_capabilities(g)
    environments_map = _extract_environments(g)
    objectives_map = _extract_objectives(g)
    human_agents_map = _extract_human_agents(g)
    resources_map = _extract_resources(g)
    constraints_map = _extract_constraints(g)

    # Cross-ontology linking
    _link_agent_relations(g, agents_map, tools_map, capabilities_map)
    _link_task_relations(g, tasks_map)
    _link_tool_relations(g, tools_map, capabilities_map)
    _link_workflow_relations(g, workflows)

    # Compute human_input flag once, centrally
    _apply_human_input_flags(tasks_map, human_agents_map)

    # Sort tasks by workflow step order
    if workflow_steps:
        step_order = {s_.task_iri: s_.step_order for s_ in workflow_steps}
        task_list = sorted(
            tasks_map.values(),
            key=lambda t: step_order.get(t.iri, 999),
        )
    else:
        task_list = list(tasks_map.values())

    # Store orchestration mode so adapters can interpret it
    if orchestration_mode and ORCHESTRATION_CONFIG_KEY not in system_configs:
        system_configs[ORCHESTRATION_CONFIG_KEY] = orchestration_mode

    project = AgenticProject(
        name=project_name,
        var_name=project_var_name,
        description=description,
        team_iri=team_iri,
        agents=list(agents_map.values()),
        tasks=task_list,
        tools=list(tools_map.values()),
        workflows=workflows,
        memories=list(memories_map.values()),
        language_models=list(lm_map.values()),
        env_vars=_extract_env_vars(g),
        system_configs=system_configs,
        goals=list(goals_map.values()),
        capabilities=list(capabilities_map.values()),
        environments=list(environments_map.values()),
        objectives=list(objectives_map.values()),
        human_agents=list(human_agents_map.values()),
        resources=list(resources_map.values()),
        constraints=list(constraints_map.values()),
    )

    # Team-level relationship linking (needs project ref)
    _link_team_relations(g, project, team_iri)

    logger.info(
        "[Extracted] project=%s  agents=%d  tasks=%d  tools=%d  "
        "workflows=%d  goals=%d  capabilities=%d  environments=%d  "
        "objectives=%d  human_agents=%d  resources=%d  constraints=%d",
        project.name,
        len(project.agents),
        len(project.tasks),
        len(project.tools),
        len(project.workflows),
        len(project.goals),
        len(project.capabilities),
        len(project.environments),
        len(project.objectives),
        len(project.human_agents),
        len(project.resources),
        len(project.constraints),
    )
    # Keep backward-compat console output for existing run.py scripts
    print(
        f"  [Extracted] project={project.name}, "
        f"{len(project.agents)} agents, "
        f"{len(project.tasks)} tasks, "
        f"{len(project.tools)} tools, "
        f"{len(project.workflows)} workflows, "
        f"{len(project.goals)} goals, "
        f"{len(project.capabilities)} capabilities, "
        f"{len(project.environments)} environments, "
        f"{len(project.objectives)} objectives, "
        f"{len(project.human_agents)} human_agents, "
        f"{len(project.resources)} resources, "
        f"{len(project.constraints)} constraints"
    )
    return project
