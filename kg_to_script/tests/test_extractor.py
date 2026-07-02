"""
Tests for the ontology coverage extraction layer.

Each test creates a minimal in-memory TTL graph and runs the
relevant extraction function, then asserts on the resulting models.
"""

from __future__ import annotations

from rdflib import Graph

from src.core.extractor import (
    _extract_goals,
    _extract_capabilities,
    _extract_environments,
    _extract_objectives,
    _extract_human_agents,
    _extract_resources,
    _extract_constraints,
    _extract_team,
    _extract_language_models,
    _extract_tools,
    _extract_memories,
    _extract_workflow_patterns,
    _extract_workflow,
    _extract_tasks,
    _extract_agents,
    _link_agent_relations,
    _link_task_relations,
    _link_tool_relations,
    _link_workflow_relations,
    extract_project,
)
from src.core.models import (
    AgentModel,
    LanguageModelModel,
    ToolModel,
)


P = "http://www.w3id.org/agentic-ai/onto#"
DC = "http://purl.org/dc/terms/"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
BEAM = "http://w3id.org/beam/core#"


def _graph(ttl: str) -> Graph:
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return g


TTL_GOALS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:goal_create_game a :Goal ;
    rdfs:label "Create Game" ;
    dcterms:description "Build a working game" .

:goal_test_code a :Goal ;
    rdfs:label "Test Code" ;
    dcterms:description "Verify correctness" .
"""


def test_extract_goals():
    g = _graph(TTL_GOALS)
    goals = _extract_goals(g)
    assert len(goals) == 2
    assert f"{P}goal_create_game" in goals
    g1 = goals[f"{P}goal_create_game"]
    assert g1.label == "Create Game"
    assert g1.description == "Build a working game"
    g2 = goals[f"{P}goal_test_code"]
    assert g2.label == "Test Code"


TTL_CAPABILITIES = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:cap_search a :Capability ;
    rdfs:label "web search" ;
    rdfs:comment "Search the web" .
"""


def test_extract_capabilities():
    g = _graph(TTL_CAPABILITIES)
    caps = _extract_capabilities(g)
    assert len(caps) == 1
    c = caps[f"{P}cap_search"]
    assert c.label == "web search"
    assert c.description == "Search the web"


TTL_ENVIRONMENTS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix beam: <http://w3id.org/beam/core#> .

:dev_env a :Environment ;
    rdfs:label "Dev" ;
    dcterms:description "Development sandbox" ;
    :envType "virtual" ;
    :hasEnvironmentConfig :env_cfg ;
    :containsResource :db_resource .

:env_cfg a :Config ;
    :configKey "region" ;
    :configValue "us-east-1" .

:db_resource a beam:Resource ;
    rdfs:label "database" .
"""


def test_extract_environments():
    g = _graph(TTL_ENVIRONMENTS)
    envs = _extract_environments(g)
    assert len(envs) == 1
    e = envs[f"{P}dev_env"]
    assert e.label == "Dev"
    assert e.env_type == "virtual"
    assert e.configs == {"region": "us-east-1"}
    assert e.contained_resource_iris == [f"{P}db_resource"]


TTL_OBJECTIVES = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:obj_main a :Objective ;
    rdfs:label "Main Objective" ;
    dcterms:description "Handle user query" ;
    :contributesToGoal :goal_help .

:goal_help a :Goal .
"""


def test_extract_objectives():
    g = _graph(TTL_OBJECTIVES)
    objs = _extract_objectives(g)
    assert len(objs) == 1
    o = objs[f"{P}obj_main"]
    assert o.label == "Main Objective"
    assert o.contributes_to_goal_iri == f"{P}goal_help"


TTL_HUMAN_AGENTS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .

:human_reviewer a :HumanAgent ;
    :agentRole "reviewer" ;
    :humanParticipatedIn :task_1 .

:task_1 a :Task .
"""


def test_extract_human_agents():
    g = _graph(TTL_HUMAN_AGENTS)
    humans = _extract_human_agents(g)
    assert len(humans) == 1
    h = humans[f"{P}human_reviewer"]
    assert h.role == "reviewer"
    assert h.participated_task_iris == [f"{P}task_1"]


TTL_RESOURCES = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix beam: <http://w3id.org/beam/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:output_data a beam:Resource ;
    rdfs:label "output" ;
    dcterms:description "Task output" .

:user_input a beam:Instance ;
    rdfs:label "input" ;
    dcterms:description "User input" .
"""


def test_extract_resources():
    g = _graph(TTL_RESOURCES)
    resources = _extract_resources(g)
    assert len(resources) == 2
    r1 = resources[f"{P}output_data"]
    assert r1.label == "output"
    assert r1.resource_type == "Resource"
    r2 = resources[f"{P}user_input"]
    assert r2.resource_type == "Instance"


TTL_CONSTRAINTS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:max_tokens a :Constraint ;
    rdfs:label "Max Tokens" ;
    dcterms:description "Limit output tokens" ;
    :hasConfig :cfg1 .

:cfg1 a :Config ;
    :configKey "limit" ;
    :configValue "4000" .
"""


def test_extract_constraints():
    g = _graph(TTL_CONSTRAINTS)
    constraints = _extract_constraints(g)
    assert len(constraints) == 1
    c = constraints[f"{P}max_tokens"]
    assert c.label == "Max Tokens"
    assert c.configs == {"limit": "4000"}


# ── Agent relationship linking ──

TTL_AGENT_RELATIONS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:agent_a a :LLMAgent ;
    :agentRole "Writer" ;
    :interactsWith :agent_b ;
    :operatesIn :env_sandbox ;
    :hasAgentCapability :cap_write ;
    :hasObjective :obj_finish .

:agent_b a :LLMAgent ;
    :agentRole "Reviewer" .

:env_sandbox a :Environment .
:cap_write a :Capability .
:obj_finish a :Objective .
"""


def test_agent_relations():
    g = _graph(TTL_AGENT_RELATIONS)
    lm_map: dict = {}
    tools_map: dict = {}
    agents = _extract_agents(g, tools_map, lm_map)
    caps_map = _extract_capabilities(g)
    _link_agent_relations(g, agents, tools_map, caps_map)

    a = agents[f"{P}agent_a"]
    assert a.interacts_with == [f"{P}agent_b"]
    assert a.operates_in_iri == f"{P}env_sandbox"
    assert a.capability_iris == [f"{P}cap_write"]
    assert a.objective_iris == [f"{P}obj_finish"]


# ── Task relationship linking ──

TTL_TASK_RELATIONS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

:task_code a :Task ;
    dcterms:description "Write code" ;
    :contributesToObjective :obj_build ;
    :requiresCapability :cap_python ;
    :performedBy :tool_compiler .

:tool_compiler a :Tool .
:obj_build a :Objective .
:cap_python a :Capability .
"""


def test_task_relations():
    g = _graph(TTL_TASK_RELATIONS)
    agents_map: dict = {}
    tasks = _extract_tasks(g, agents_map)
    _link_task_relations(g, tasks)

    t = tasks[f"{P}task_code"]
    assert t.contributes_to_objective_iri == f"{P}obj_build"
    assert t.requires_capability_iris == [f"{P}cap_python"]
    assert t.performed_by_iri == f"{P}tool_compiler"


# ── Tool relationship linking ──

TTL_TOOL_RELATIONS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix beam: <http://w3id.org/beam/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:search_tool a :Tool ;
    rdfs:label "search" ;
    :hasCapability :cap_search ;
    :resourceUsage :web_resource ;
    :toolUsage :parse_tool .

:cap_search a :Capability .
:web_resource a beam:Resource .
:parse_tool a :Tool .
"""


def test_tool_relations():
    g = _graph(TTL_TOOL_RELATIONS)
    tools = _extract_tools(g)
    caps_map = _extract_capabilities(g)
    _link_tool_relations(g, tools, caps_map)

    t = tools[f"{P}search_tool"]
    assert t.capability_iris == [f"{P}cap_search"]
    assert t.resource_usage_iris == [f"{P}web_resource"]
    assert t.tool_usage_iris == [f"{P}parse_tool"]


# ── Workflow pattern relationship linking ──

TTL_WORKFLOW_RELATIONS = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

:wp_main a :WorkflowPattern ;
    dcterms:description "Main flow" ;
    :hasRelatedPattern :wp_sub ;
    :nextPattern :wp_next .

:wp_sub a :WorkflowPattern .
:wp_next a :WorkflowPattern .
"""
# Note: hasRelatedPattern without hasSubPattern check is tested below


def test_workflow_pattern_relations():
    g = _graph(TTL_WORKFLOW_RELATIONS)
    tasks_map: dict = {}
    steps = _extract_workflow(g, tasks_map)
    patterns = _extract_workflow_patterns(g, steps, "sequential")
    _link_workflow_relations(g, patterns)

    wp = [p for p in patterns if p.iri == f"{P}wp_main"][0]
    assert f"{P}wp_sub" in wp.related_pattern_iris
    assert wp.next_pattern_iri == f"{P}wp_next"


# ── Agent goal_iri ──

TTL_AGENT_GOAL = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

:agent_a a :LLMAgent ;
    :agentRole "Engineer" ;
    :hasAgentGoal :goal_build .

:goal_build a :Goal ;
    dcterms:description "Build the product" .
"""


def test_agent_goal_iri():
    g = _graph(TTL_AGENT_GOAL)
    agents = _extract_agents(g, {}, {})
    a = agents[f"{P}agent_a"]
    assert a.goal_iri == f"{P}goal_build"
    assert a.goal == "Build the product"


# ── Empty results ──

TTL_EMPTY = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
"""


def test_extract_goals_empty():
    assert _extract_goals(_graph(TTL_EMPTY)) == {}


def test_extract_capabilities_empty():
    assert _extract_capabilities(_graph(TTL_EMPTY)) == {}


def test_extract_environments_empty():
    assert _extract_environments(_graph(TTL_EMPTY)) == {}


def test_extract_objectives_empty():
    assert _extract_objectives(_graph(TTL_EMPTY)) == {}


def test_extract_human_agents_empty():
    assert _extract_human_agents(_graph(TTL_EMPTY)) == {}


def test_extract_resources_empty():
    assert _extract_resources(_graph(TTL_EMPTY)) == {}


def test_extract_constraints_empty():
    assert _extract_constraints(_graph(TTL_EMPTY)) == {}


# ── Integration test: end-to-end with real KG ──

TTL_INTEGRATION = """
@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix beam: <http://w3id.org/beam/core#> .

:my_team a :Team ;
    rdfs:label "MyTeam" ;
    dcterms:description "Test team" ;
    :hasAgentMember :agent_alice, :agent_bob ;
    :hasWorkflowPattern :wp_test ;
    :hasTeamGoal :goal_win .

:goal_win a :Goal ;
    rdfs:label "Win" ;
    dcterms:description "Win the game" .

:agent_alice a :LLMAgent ;
    :agentRole "Leader" ;
    :hasAgentGoal :goal_win ;
    :interactsWith :agent_bob .

:agent_bob a :LLMAgent ;
    :agentRole "Follower" ;
    :hasAgentGoal :goal_win .

:cap_search a :Capability ;
    rdfs:label "search" .

:tool_web a :Tool ;
    rdfs:label "WebTool" ;
    :hasCapability :cap_search .

:task_1 a :Task ;
    dcterms:description "Do research" ;
    :performedByAgent :agent_alice ;
    :requiresCapability :cap_search .

:step_start a :StartStep ;
    :hasAssociatedTask :task_1 ;
    :stepOrder 1 .

:wp_test a :WorkflowPattern ;
    :hasWorkflowStep :step_start .
"""


def test_integration_full_coverage():
    g = _graph(TTL_INTEGRATION)
    project = extract_project.__wrapped__(g) if hasattr(extract_project, '__wrapped__') else None

    # Manual pipeline to avoid file path requirement
    from src.core.extractor import load_graph

    # Use the graph directly to mimic extract_project
    project_name, description, process, team_iri = _extract_team(g, {})
    tools_map = _extract_tools(g)
    agents_map = _extract_agents(g, tools_map, {})
    tasks_map = _extract_tasks(g, agents_map)
    workflow_steps = _extract_workflow(g, tasks_map)
    workflows = _extract_workflow_patterns(g, workflow_steps, process)
    goals_map = _extract_goals(g)
    capabilities_map = _extract_capabilities(g)
    environments_map = _extract_environments(g)
    objectives_map = _extract_objectives(g)
    human_agents_map = _extract_human_agents(g)
    resources_map = _extract_resources(g)
    constraints_map = _extract_constraints(g)
    _link_agent_relations(g, agents_map, tools_map, capabilities_map)
    _link_task_relations(g, tasks_map)
    _link_tool_relations(g, tools_map, capabilities_map)
    _link_workflow_relations(g, workflows)

    from src.core.models import AgenticProject
    from src.core.extractor import _link_team_relations

    project = AgenticProject(
        name=project_name,
        description=description,
        team_iri=team_iri,
        agents=list(agents_map.values()),
        tasks=list(tasks_map.values()),
        tools=list(tools_map.values()),
        workflows=workflows,
        goals=list(goals_map.values()),
        capabilities=list(capabilities_map.values()),
        environments=list(environments_map.values()),
        objectives=list(objectives_map.values()),
        human_agents=list(human_agents_map.values()),
        resources=list(resources_map.values()),
        constraints=list(constraints_map.values()),
    )
    _link_team_relations(g, project, team_iri)

    assert project.name == "MyTeam"
    assert project.team_iri == f"{P}my_team"
    assert len(project.agent_member_iris) == 2
    assert f"{P}agent_alice" in project.agent_member_iris
    assert project.workflow_pattern_iris == [f"{P}wp_test"]
    assert project.goal_iris == [f"{P}goal_win"]

    assert len(project.goals) == 1
    assert project.goals[0].label == "Win"

    assert len(project.capabilities) == 1
    assert project.capabilities[0].label == "search"

    assert len(project.tools) == 1
    tool = project.tools[0]
    assert tool.label == "WebTool"
    assert tool.capability_iris == [f"{P}cap_search"]

    assert len(project.agents) == 2
    alice = [a for a in project.agents if a.var_name == "agent_alice"][0]
    assert alice.role == "Leader"
    assert alice.goal_iri == f"{P}goal_win"
    assert alice.interacts_with == [f"{P}agent_bob"]

    assert len(project.tasks) == 1
    task = project.tasks[0]
    assert task.requires_capability_iris == [f"{P}cap_search"]
