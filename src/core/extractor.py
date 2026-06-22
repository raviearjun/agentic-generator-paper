from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from rdflib import Graph

from .models import (
    AgenticProject,
    AgentModel,
    CapabilityModel,
    ConfigModel,
    ConstraintModel,
    EnvironmentModel,
    GoalModel,
    HumanAgentModel,
    InputVariableModel,
    LanguageModelModel,
    MemoryModel,
    ObjectiveModel,
    ProcessType,
    ResourceModel,
    TaskModel,
    ToolConfigModel,
    ToolModel,
    WorkflowPatternModel,
    WorkflowStepModel,
    WorkflowType,
)


# ─────────────────────── Helpers ───────────────────────

def _s(val: Any) -> str:
    """Convert rdflib term to stripped str."""
    return str(val).strip() if val else ""


def _safe_var(iri: str) -> str:
    """
    IRI fragment → valid Python snake_case identifier.

    e.g. "http://…/onto#SeniorEngineerAgent" → "senior_engineer_agent"
    """
    if not iri:
        return "unnamed"
    name = iri.split("/")[-1].split("#")[-1]
    # Insert _ before uppercase runs: "SeniorEngineer" → "Senior_Engineer"
    name = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name)
    name = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", name)
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_").lower()
    if not name:
        return "unnamed"
    if name[0].isdigit():
        name = f"_{name}"
    return name


def _camel(s: str) -> str:
    """snake_case → CamelCase: 'game_builder_crew' → 'GameBuilderCrew'."""
    return "".join(w.capitalize() for w in s.split("_"))


def _extract_placeholders(text: str) -> List[str]:
    """Extract {placeholder} variable names from a string."""
    return list(dict.fromkeys(re.findall(r"\{(\w+)\}", text)))


def load_graph(file_path: str) -> Graph:
    """Parse a Turtle (.ttl) file into an rdflib Graph."""
    g = Graph()
    g.parse(file_path, format="turtle")
    return g


# ─────────────────────── SPARQL Queries ───────────────────────

PREFIXES = """\
PREFIX : <http://www.w3id.org/agentic-ai/onto#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX beam:    <http://w3id.org/beam/core#>
"""

# ── Team ──

TEAM_QUERY = PREFIXES + """
SELECT ?team ?label ?desc
WHERE {
    ?team a :Team .
    OPTIONAL { ?team rdfs:label ?label }
    OPTIONAL { ?team dcterms:description ?desc }
}
"""

TEAM_PROCESS_QUERY = PREFIXES + """
SELECT ?configValue
WHERE {
    ?team a :Team ;
          :hasSystemConfig ?cfg .
    ?cfg :configKey "process" ;
         :configValue ?configValue .
}
"""

# Fallback: detect process type from WorkflowPattern label/desc or Team desc
WORKFLOW_PATTERN_TEXT_QUERY = PREFIXES + """
SELECT ?label ?desc ?comment ?title
WHERE {
    ?wp a :WorkflowPattern .
    OPTIONAL { ?wp rdfs:label ?label }
    OPTIONAL { ?wp dcterms:description ?desc }
    OPTIONAL { ?wp rdfs:comment ?comment }
    OPTIONAL { ?wp dcterms:title ?title }
}
"""

TEAM_DESC_QUERY = PREFIXES + """
SELECT ?desc ?comment
WHERE {
    ?team a :Team .
    OPTIONAL { ?team dcterms:description ?desc }
    OPTIONAL { ?team rdfs:comment ?comment }
}
"""

# ── Language Models ──

LLM_QUERY = PREFIXES + """
SELECT DISTINCT ?lm ?label ?desc
WHERE {
    ?lm a :LanguageModel .
    OPTIONAL { ?lm rdfs:label ?label }
    OPTIONAL { ?lm dcterms:description ?desc }
}
"""

# ── Tools (exclude LLMAgent which is subclass of Tool) ──

TOOLS_QUERY = PREFIXES + """
SELECT DISTINCT ?tool ?label ?desc ?comment
WHERE {
    ?tool a :Tool .
    FILTER NOT EXISTS { ?tool a :LLMAgent }
    OPTIONAL { ?tool rdfs:label ?label }
    OPTIONAL { ?tool dcterms:description ?desc }
    OPTIONAL { ?tool rdfs:comment ?comment }
}
"""

TOOL_CONFIGS_QUERY = PREFIXES + """
SELECT ?tool ?key ?value
WHERE {
    ?tool a :Tool ;
          :hasToolConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
    FILTER NOT EXISTS { ?tool a :LLMAgent }
}
"""

# ── Agents (canonical pattern — single consolidated query) ──
# Extracts all single-valued agent properties in one pass:
#   role, goal, backstory, allow_delegation, verbose
# Multi-valued relations (tools, LLM) remain as separate queries.

AGENTS_QUERY = PREFIXES + """
SELECT DISTINCT ?agent ?agentID ?role ?label ?goal ?goalDesc ?backstory
                ?delegation ?verbose
WHERE {
    ?agent a :LLMAgent .
    OPTIONAL { ?agent :agentID ?agentID }
    OPTIONAL { ?agent :agentRole ?role }
    OPTIONAL { ?agent rdfs:label ?label }
    OPTIONAL {
        ?agent :hasAgentGoal ?goal .
        ?goal dcterms:description ?goalDesc .
    }
    OPTIONAL {
        ?agent :agentPrompt ?prompt .
        ?prompt :promptContext ?backstory .
    }
    OPTIONAL {
        ?agent :hasAgentConfig ?cfgD .
        ?cfgD :configKey "allow_delegation" ;
              :configValue ?delegation .
    }
    OPTIONAL {
        ?agent :hasAgentConfig ?cfgV .
        ?cfgV :configKey "verbose" ;
              :configValue ?verbose .
    }
}
"""

AGENT_TOOLS_QUERY = PREFIXES + """
SELECT DISTINCT ?agent ?tool
WHERE {
    ?agent a :LLMAgent ;
           :agentToolUsage ?tool .
    ?tool a :Tool .
    FILTER NOT EXISTS { ?tool a :LLMAgent }
}
"""

AGENT_LLM_QUERY = PREFIXES + """
SELECT DISTINCT ?agent ?lm
WHERE {
    ?agent a :LLMAgent ;
           :useLanguageModel ?lm .
}
"""

AGENT_ALL_CONFIGS_QUERY = PREFIXES + """
SELECT ?agent ?key ?value
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

AGENT_KNOWLEDGE_QUERY = PREFIXES + """
SELECT DISTINCT ?agent ?knowledge
WHERE {
    ?agent a :LLMAgent ;
           :hasKnowledge ?knowledge .
}
"""



# ── Tasks ──

TASKS_QUERY = PREFIXES + """
SELECT DISTINCT ?task ?label ?desc ?agent
WHERE {
    ?task a :Task .
    OPTIONAL { ?task rdfs:label ?label }
    OPTIONAL { ?task dcterms:description ?desc }
    OPTIONAL { ?task :performedByAgent ?agent }
}
"""

TASK_PROMPT_QUERY = PREFIXES + """
SELECT ?task ?instruction ?inputData ?outputIndicator ?context
WHERE {
    ?task a :Task .
    {
        { ?task :taskPrompt ?prompt }
        UNION
        { ?task :hasPrompt ?prompt }
    }
    ?prompt a :Prompt .
    OPTIONAL { ?prompt :promptInstruction ?instruction }
    OPTIONAL { ?prompt :promptInputData ?inputData }
    OPTIONAL { ?prompt :promptOutputIndicator ?outputIndicator }
    OPTIONAL { ?prompt :promptContext ?context }
}
"""

TASK_CONFIG_QUERY = PREFIXES + """
SELECT ?task ?key ?value
WHERE {
    ?task a :Task ;
          :hasAgentConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

TASK_EXPECTED_CONFIG_QUERY = PREFIXES + """
SELECT ?task ?value
WHERE {
    ?task a :Task ;
          :hasAgentConfig ?cfg .
    ?cfg :configKey "expected_output" ;
         :configValue ?value .
}
"""

TASK_DESCRIPTION_CONFIG_QUERY = PREFIXES + """
SELECT ?task ?value
WHERE {
    ?task a :Task ;
          :hasAgentConfig ?cfg .
    ?cfg :configKey "description" ;
         :configValue ?value .
}
"""

# ── Task Context (resource dependencies) ──

TASK_PRODUCES_QUERY = PREFIXES + """
SELECT ?task ?resource
WHERE {
    ?task a :Task ;
          :producedResource ?resource .
}
"""

TASK_REQUIRES_QUERY = PREFIXES + """
SELECT ?task ?resource
WHERE {
    ?task a :Task ;
          :requiresResource ?resource .
}
"""

# ── Workflow ──

WORKFLOW_QUERY = PREFIXES + """
SELECT ?step ?stepOrder ?task ?stepType
WHERE {
    ?step :hasAssociatedTask ?task .
    ?step a ?stepType .
    VALUES ?stepType { :WorkflowStep :StartStep :EndStep }
    OPTIONAL { ?step :stepOrder ?stepOrder }
}
ORDER BY ?stepOrder
"""

WORKFLOW_PATTERN_QUERY = PREFIXES + """
SELECT ?wp ?label ?desc
WHERE {
    ?wp a :WorkflowPattern .
    OPTIONAL { ?wp rdfs:label ?label }
    OPTIONAL { ?wp dcterms:description ?desc }
}
"""

WORKFLOW_STEPS_QUERY = PREFIXES + """
SELECT ?wp ?step
WHERE {
    ?wp a :WorkflowPattern ;
        :hasWorkflowStep ?step .
}
"""

WORKFLOW_SUB_PATTERN_QUERY = PREFIXES + """
SELECT ?wp ?sub
WHERE {
    ?wp :hasSubPattern ?sub .
    ?sub a :WorkflowPattern .
}
"""

STEP_EDGES_QUERY = PREFIXES + """
SELECT ?source ?target
WHERE {
    ?source :nextStep ?target .
}
"""

MEMORY_QUERY = PREFIXES + """
SELECT DISTINCT ?mem ?label ?desc
WHERE {
    ?mem a :Memory .
    OPTIONAL { ?mem rdfs:label ?label }
    OPTIONAL { ?mem dcterms:description ?desc }
}
"""

MEMORY_CONFIG_QUERY = PREFIXES + """
SELECT ?mem ?key ?value
WHERE {
    ?mem a :Memory ;
         :hasConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

SYSTEM_CONFIG_QUERY = PREFIXES + """
SELECT ?key ?value
WHERE {
    ?team a :Team ;
          :hasSystemConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

# ── Input Variables (from prompt input data) ──

PROMPT_INPUT_DATA_QUERY = PREFIXES + """
SELECT DISTINCT ?inputData
WHERE {
    ?prompt a :Prompt ;
            :promptInputData ?inputData .
}
"""

# ── Default inputs (from :Context / beam:Resource) — LEGACY fallback ──

DEFAULT_INPUTS_QUERY = PREFIXES + """
SELECT ?resource ?desc
WHERE {
    {
        ?resource a beam:Resource .
        ?resource dcterms:description ?desc .
        FILTER(CONTAINS(LCASE(STR(?desc)), "input"))
    }
    UNION
    {
        ?resource a :Context .
        ?resource dcterms:description ?desc .
        FILTER(CONTAINS(LCASE(STR(?desc)), "input"))
    }
}
"""

# ── Uniform inputs (agento-ext:KickoffInputBundle) — PRIMARY ──

KICKOFF_INPUTS_QUERY = PREFIXES + """
PREFIX agento_ext: <http://www.w3id.org/agentic-ai/ext#>
SELECT ?key ?value ?isDefault
WHERE {
    ?bundle a agento_ext:KickoffInputBundle ;
            agento_ext:inputKey ?key ;
            agento_ext:inputValue ?value ;
            agento_ext:isDefaultValue ?isDefault .
}
"""

# ── Environment config (API keys) ──

ENV_CONFIG_QUERY = PREFIXES + """
SELECT ?key ?value
WHERE {
    ?cfg a :Config ;
         :configKey ?key ;
         :configValue ?value .
    FILTER(CONTAINS(LCASE(?key), "api_key") || CONTAINS(LCASE(?key), "env"))
}
"""


# ── Goals (standalone :Goal individuals) ──

GOALS_QUERY = PREFIXES + """
SELECT DISTINCT ?goal ?label ?desc
WHERE {
    ?goal a :Goal .
    OPTIONAL { ?goal rdfs:label ?label }
    OPTIONAL { ?goal dcterms:description ?desc }
}
"""

# ── Capabilities (standalone :Capability individuals) ──

CAPABILITIES_QUERY = PREFIXES + """
SELECT DISTINCT ?cap ?label ?desc ?comment
WHERE {
    ?cap a :Capability .
    OPTIONAL { ?cap rdfs:label ?label }
    OPTIONAL { ?cap dcterms:description ?desc }
    OPTIONAL { ?cap rdfs:comment ?comment }
}
"""

# ── Environments ──

ENVIRONMENTS_QUERY = PREFIXES + """
SELECT DISTINCT ?env ?label ?desc ?envType
WHERE {
    ?env a :Environment .
    OPTIONAL { ?env rdfs:label ?label }
    OPTIONAL { ?env dcterms:description ?desc }
    OPTIONAL { ?env :envType ?envType }
}
"""

ENVIRONMENT_CONFIGS_QUERY = PREFIXES + """
SELECT ?env ?key ?value
WHERE {
    ?env a :Environment ;
          :hasEnvironmentConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

ENVIRONMENT_CONTAINS_QUERY = PREFIXES + """
SELECT ?env ?resource
WHERE {
    ?env a :Environment ;
          :containsResource ?resource .
}
"""

# ── Objectives ──

OBJECTIVES_QUERY = PREFIXES + """
SELECT DISTINCT ?obj ?label ?desc ?goal
WHERE {
    ?obj a :Objective .
    OPTIONAL { ?obj rdfs:label ?label }
    OPTIONAL { ?obj dcterms:description ?desc }
    OPTIONAL { ?obj :contributesToGoal ?goal }
}
"""

# ── Human Agents ──

HUMAN_AGENTS_QUERY = PREFIXES + """
SELECT DISTINCT ?human ?role
WHERE {
    ?human a :HumanAgent .
    OPTIONAL { ?human :agentRole ?role }
}
"""

HUMAN_PARTICIPATED_QUERY = PREFIXES + """
SELECT ?human ?task
WHERE {
    ?human a :HumanAgent ;
           :humanParticipatedIn ?task .
}
"""

# ── Resources (beam:Resource and subclasses) ──

RESOURCES_QUERY = PREFIXES + """
SELECT DISTINCT ?res ?label ?desc ?type
WHERE {
    VALUES ?type { beam:Resource beam:Instance }
    ?res a ?type .
    OPTIONAL { ?res rdfs:label ?label }
    OPTIONAL { ?res dcterms:description ?desc }
}
"""

# ── Constraints —─

CONSTRAINTS_QUERY = PREFIXES + """
SELECT DISTINCT ?con ?label ?desc
WHERE {
    ?con a :Constraint .
    OPTIONAL { ?con rdfs:label ?label }
    OPTIONAL { ?con dcterms:description ?desc }
}
"""

CONSTRAINT_CONFIGS_QUERY = PREFIXES + """
SELECT ?con ?key ?value
WHERE {
    ?con a :Constraint ;
          :hasConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

# ── Agent relationship queries ──

AGENT_INTERACTS_QUERY = PREFIXES + """
SELECT ?agent ?target
WHERE {
    ?agent a :LLMAgent ;
           :interactsWith ?target .
}
"""

AGENT_OPERATES_IN_QUERY = PREFIXES + """
SELECT ?agent ?env
WHERE {
    ?agent a :LLMAgent ;
           :operatesIn ?env .
}
"""

AGENT_CAPABILITY_QUERY = PREFIXES + """
SELECT ?agent ?cap
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentCapability ?cap .
}
"""

AGENT_OBJECTIVE_QUERY = PREFIXES + """
SELECT ?agent ?obj
WHERE {
    ?agent a :LLMAgent ;
           :hasObjective ?obj .
}
"""

# ── Task relationship queries ──

TASK_OBJECTIVE_QUERY = PREFIXES + """
SELECT ?task ?obj
WHERE {
    ?task a :Task ;
           :contributesToObjective ?obj .
}
"""

TASK_PERFORMED_BY_QUERY = PREFIXES + """
SELECT ?task ?performer
WHERE {
    ?task a :Task ;
           :performedBy ?performer .
    FILTER NOT EXISTS { ?performer a :LLMAgent }
}
"""

TASK_CAPABILITY_QUERY = PREFIXES + """
SELECT ?task ?cap
WHERE {
    ?task a :Task ;
           :requiresCapability ?cap .
}
"""

# ── Tool relationship queries ──

TOOL_CAPABILITY_QUERY = PREFIXES + """
SELECT ?tool ?cap
WHERE {
    ?tool a :Tool ;
          :hasCapability ?cap .
    FILTER NOT EXISTS { ?tool a :LLMAgent }
}
"""

TOOL_RESOURCE_USAGE_QUERY = PREFIXES + """
SELECT ?tool ?resource
WHERE {
    ?tool a :Tool ;
          :resourceUsage ?resource .
    FILTER NOT EXISTS { ?tool a :LLMAgent }
}
"""

TOOL_TOOL_USAGE_QUERY = PREFIXES + """
SELECT ?tool ?child
WHERE {
    ?tool a :Tool ;
          :toolUsage ?child .
    FILTER NOT EXISTS { ?tool a :LLMAgent }
}
"""

# ── Team relationship queries ──

TEAM_AGENT_MEMBERS_QUERY = PREFIXES + """
SELECT ?team ?agent
WHERE {
    ?team a :Team ;
          :hasAgentMember ?agent .
}
"""

TEAM_WORKFLOW_PATTERN_QUERY = PREFIXES + """
SELECT ?team ?wp
WHERE {
    ?team a :Team ;
          :hasWorkflowPattern ?wp .
}
"""

TEAM_GOAL_QUERY = PREFIXES + """
SELECT ?team ?goal
WHERE {
    ?team a :Team ;
          :hasGoal ?goal .
}
"""

TEAM_TEAM_GOAL_QUERY = PREFIXES + """
SELECT ?team ?goal
WHERE {
    ?team a :Team ;
          :hasTeamGoal ?goal .
}
"""

TEAM_OBJECTIVE_QUERY = PREFIXES + """
SELECT ?team ?obj
WHERE {
    ?team a :Team ;
          :hasObjective ?obj .
}
"""

# ── Workflow pattern relationship queries ──

WORKFLOW_RELATED_PATTERN_QUERY = PREFIXES + """
SELECT ?wp ?related
WHERE {
    ?wp a :WorkflowPattern ;
        :hasRelatedPattern ?related .
    FILTER NOT EXISTS { ?wp :hasSubPattern ?related }
}
"""

WORKFLOW_NEXT_PATTERN_QUERY = PREFIXES + """
SELECT ?wp ?next
WHERE {
    ?wp a :WorkflowPattern ;
        :nextPattern ?next .
}
"""

# ─────────────────────── Extraction functions ───────────────────────

def _infer_process_from_text(text: str) -> Optional[ProcessType]:
    """
    Infer process type from free-text label/description/comment.

    Checks for 'hierarchical' first (rarer, more specific),
    then 'sequential'.  Returns None if neither keyword found.
    """
    if not text:
        return None
    lower = text.lower()
    if "hierarchical" in lower:
        return ProcessType.HIERARCHICAL
    if "sequential" in lower:
        return ProcessType.SEQUENTIAL
    return None




# ── Strategy 1.5 helpers removed: canonical KG uses separate Config per key ──


def _extract_team(g: Graph) -> Tuple[str, str, ProcessType, str]:
    """Extract team name, description, process type, and team IRI."""
    crew_name = "MyCrew"
    description = ""
    process = ProcessType.SEQUENTIAL
    team_iri = ""

    results = list(g.query(TEAM_QUERY))
    if results:
        row = results[0]
        team_iri = _s(row.team)
        label = _s(row.label)
        if label:
            # Use label as crew class name, cleaned to CamelCase
            crew_name = re.sub(r"[^a-zA-Z0-9]", "", label)
            if not crew_name:
                crew_name = "MyCrew"
        description = _s(row.desc)

    # ── Strategy 1: explicit configKey "process" (most authoritative) ──
    process_results = list(g.query(TEAM_PROCESS_QUERY))
    detected = False
    for row in process_results:
        val = _s(row.configValue).lower()
        if "hierarchical" in val:
            process = ProcessType.HIERARCHICAL
            detected = True
        elif "sequential" in val:
            process = ProcessType.SEQUENTIAL
            detected = True

    # ── Strategy 2: WorkflowPattern labels/descriptions (common fallback) ──
    if not detected:
        for row in g.query(WORKFLOW_PATTERN_TEXT_QUERY):
            for field_val in [_s(row.label), _s(row.desc), _s(row.comment), _s(row.title)]:
                inferred = _infer_process_from_text(field_val)
                if inferred is not None:
                    process = inferred
                    detected = True
                    # Hierarchical is rarer and more specific — if found, stop
                    if inferred == ProcessType.HIERARCHICAL:
                        break
            if detected and process == ProcessType.HIERARCHICAL:
                break

    # ── Strategy 3: Team description/comment text ──
    if not detected:
        for row in g.query(TEAM_DESC_QUERY):
            for field_val in [_s(row.desc), _s(row.comment)]:
                inferred = _infer_process_from_text(field_val)
                if inferred is not None:
                    process = inferred
                    detected = True
                    break
            if detected:
                break

    return crew_name, description, process, team_iri


def _extract_language_models(g: Graph) -> Dict[str, LanguageModelModel]:
    """Extract LanguageModel individuals keyed by IRI."""
    models: Dict[str, LanguageModelModel] = {}
    for row in g.query(LLM_QUERY):
        iri = _s(row.lm)
        label = _s(row.label)
        desc = _s(row.desc)

        # Infer provider and model_name from label/description
        provider = ""
        model_name = ""
        text = f"{label} {desc}".lower()
        if "ollama" in text:
            provider = "ollama"
            # Try to extract model name like "llama3.1"
            m = re.search(r"ollama\S*\s*[\(\"']?([a-z0-9._-]+)", text)
            if m:
                model_name = m.group(1)
        elif "openai" in text or "gpt" in text:
            provider = "openai"
            m = re.search(r"(gpt-[a-z0-9._-]+)", text)
            if m:
                model_name = m.group(1)

        models[iri] = LanguageModelModel(
            iri=iri,
            name=label,
            description=desc,
            provider=provider,
            model_name=model_name,
        )
    return models


def _extract_tools(g: Graph) -> Dict[str, ToolModel]:
    """Extract standalone Tool individuals (excluding LLMAgent)."""
    tools: Dict[str, ToolModel] = {}

    for row in g.query(TOOLS_QUERY):
        iri = _s(row.tool)
        if iri in tools:
            continue
        label = _s(row.label)
        desc = _s(row.desc) or _s(row.comment) or ""

        # Infer class name from label
        class_name = label if label else _safe_var(iri)
        # Clean class name: remove spaces, keep CamelCase
        class_name_clean = re.sub(r"[^a-zA-Z0-9]", "", class_name)

        tools[iri] = ToolModel(
            iri=iri,
            var_name=_safe_var(iri),
            label=label,
            class_name=class_name_clean,
            description=desc.strip(),
            configs=[],
            capabilities=[],
        )

    # Tool configs
    for row in g.query(TOOL_CONFIGS_QUERY):
        iri = _s(row.tool)
        if iri in tools:
            tools[iri].configs.append(
                ToolConfigModel(key=_s(row.key), value=_s(row.value))
            )

    return tools


def _extract_agents(
    g: Graph,
    tools_map: Dict[str, ToolModel],
    lm_map: Dict[str, LanguageModelModel],
) -> Dict[str, AgentModel]:
    """Extract LLMAgent individuals from canonical KG pattern.

    Single consolidated SPARQL query extracts all scalar properties:
      role      → :agentRole literal
      goal      → :hasAgentGoal → Goal → dcterms:description
      backstory → :agentPrompt → Prompt → :promptContext
      delegation/verbose → separate Config individuals per key

    Multi-valued relations (tools, LLM) use separate queries.
    """
    agents: Dict[str, AgentModel] = {}

    for row in g.query(AGENTS_QUERY):
        iri = _s(row.agent)
        if iri in agents:
            continue
        agent_id = _s(row.agentID)
        label = _s(row.label)
        role = _s(row.role)

        var_name = agent_id or label or _safe_var(iri)
        var_name = _safe_var(var_name) if not re.match(r'^[a-z_][a-z0-9_]*$', var_name) else var_name

        # Parse allow_delegation
        deleg_val = _s(row.delegation).strip().lower()
        allow_delegation = None
        if deleg_val:
            allow_delegation = deleg_val in ("true", "1", "yes")

        # Parse verbose
        verbose_val = _s(row.verbose).strip().lower()
        verbose = None
        if verbose_val:
            verbose = verbose_val not in ("false", "0", "no", "none")

        agents[iri] = AgentModel(
            iri=iri,
            var_name=var_name,
            agent_id=agent_id,
            role=role,
            goal=_s(row.goalDesc),
            goal_iri=_s(row.goal),
            backstory=_s(row.backstory),
            system_prompt=_s(row.backstory),
            tool_iris=[],
            tool_var_names=[],
            language_model=None,
            llm=None,
            configs={},
            knowledge_iris=[],
            allow_delegation=allow_delegation,
            verbose=verbose,
        )

    # All agent configs are kept in the agnostic IR. Legacy convenience fields
    # are still populated for existing CrewAI templates.
    for row in g.query(AGENT_ALL_CONFIGS_QUERY):
        iri = _s(row.agent)
        if iri not in agents:
            continue
        key = _s(row.key)
        value = _s(row.value)
        agents[iri].configs[key] = value
        lowered = key.lower()
        if lowered == "allow_delegation" and agents[iri].allow_delegation is None:
            agents[iri].allow_delegation = value.strip().lower() in ("true", "1", "yes")
        elif lowered == "verbose" and agents[iri].verbose is None:
            agents[iri].verbose = value.strip().lower() not in ("false", "0", "no", "none")

    # Agent → Tool links (multi-valued, separate query)
    for row in g.query(AGENT_TOOLS_QUERY):
        iri = _s(row.agent)
        tool_iri = _s(row.tool)
        if iri in agents and tool_iri in tools_map:
            if tool_iri not in agents[iri].tool_iris:
                agents[iri].tool_iris.append(tool_iri)
            tool_var = tools_map[tool_iri].var_name
            if tool_var not in agents[iri].tool_var_names:
                agents[iri].tool_var_names.append(tool_var)

    # Agent → LanguageModel (multi-valued, separate query)
    for row in g.query(AGENT_LLM_QUERY):
        iri = _s(row.agent)
        lm_iri = _s(row.lm)
        if iri in agents and lm_iri in lm_map:
            agents[iri].language_model = lm_map[lm_iri]
            agents[iri].llm = lm_map[lm_iri]

    for row in g.query(AGENT_KNOWLEDGE_QUERY):
        iri = _s(row.agent)
        knowledge_iri = _s(row.knowledge)
        if iri in agents and knowledge_iri not in agents[iri].knowledge_iris:
            agents[iri].knowledge_iris.append(knowledge_iri)

    # Final defaults
    for agent in agents.values():
        if not agent.role:
            agent.role = "LLM Agent"
        if not agent.goal:
            agent.goal = agent.role
        if not agent.backstory:
            agent.backstory = f"You are a {agent.role}."
        if not agent.system_prompt:
            agent.system_prompt = agent.backstory

    return agents


def _extract_tasks(g: Graph, agents_map: Dict[str, AgentModel]) -> Dict[str, TaskModel]:
    """Extract Task individuals with full property resolution."""
    tasks: Dict[str, TaskModel] = {}

    # Reverse lookup: agent IRI → var_name
    agent_iri_to_var: Dict[str, str] = {a.iri: a.var_name for a in agents_map.values()}

    # Primary task properties
    for row in g.query(TASKS_QUERY):
        iri = _s(row.task)
        if iri in tasks:
            continue

        label = _s(row.label)
        desc = _s(row.desc)
        agent_iri = _s(row.agent)

        var_name = label or _safe_var(iri)
        var_name = _safe_var(var_name) if not re.match(r'^[a-z_][a-z0-9_]*$', var_name) else var_name

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
        iri = _s(row.task)
        if iri in tasks:
            tasks[iri].configs[_s(row.key)] = _s(row.value)

    # Task description from Config (override if richer)
    for row in g.query(TASK_DESCRIPTION_CONFIG_QUERY):
        iri = _s(row.task)
        val = _s(row.value)
        if iri in tasks:
            # Use config description if it's longer (more detailed)
            if len(val) > len(tasks[iri].description):
                tasks[iri].description = val

    # Prompt data
    for row in g.query(TASK_PROMPT_QUERY):
        iri = _s(row.task)
        if iri not in tasks:
            continue
        instr = _s(row.instruction)
        input_data = _s(row.inputData)
        output = _s(row.outputIndicator)
        context = _s(row.context)
        tasks[iri].prompt_instruction = instr
        tasks[iri].prompt_input_data = input_data
        tasks[iri].prompt_output_indicator = output
        tasks[iri].prompt_context = context
        if output and not tasks[iri].expected_output:
            tasks[iri].expected_output = output
        if instr and not tasks[iri].description:
            tasks[iri].description = instr

    # Expected output from Config
    for row in g.query(TASK_EXPECTED_CONFIG_QUERY):
        iri = _s(row.task)
        val = _s(row.value)
        if iri in tasks and not tasks[iri].expected_output:
            tasks[iri].expected_output = val

    # Final defaults
    for task in tasks.values():
        if not task.description:
            task.description = task.var_name.replace("_", " ").title()
        if not task.expected_output:
            task.expected_output = f"Completed: {task.var_name}"

    return tasks


def _resolve_task_context(g: Graph, tasks_map: Dict[str, TaskModel]) -> None:
    """
    Resolve task context dependencies via producedResource/requiresResource chains.

    If Task B requiresResource R, and Task A producedResource R,
    then Task B's context includes Task A.
    """
    # Build resource → producing task map
    resource_to_producer: Dict[str, str] = {}
    for row in g.query(TASK_PRODUCES_QUERY):
        task_iri = _s(row.task)
        res_iri = _s(row.resource)
        if task_iri in tasks_map:
            if res_iri not in tasks_map[task_iri].produced_resources:
                tasks_map[task_iri].produced_resources.append(res_iri)
            resource_to_producer[res_iri] = tasks_map[task_iri].var_name

    # For each task's required resources, find the producing task
    for row in g.query(TASK_REQUIRES_QUERY):
        task_iri = _s(row.task)
        res_iri = _s(row.resource)
        if task_iri in tasks_map:
            task = tasks_map[task_iri]
            if res_iri not in task.required_resources:
                task.required_resources.append(res_iri)
        if task_iri in tasks_map and res_iri in resource_to_producer:
            producer_var = resource_to_producer[res_iri]
            if producer_var != task.var_name and producer_var not in task.context_task_var_names:
                task.context_task_var_names.append(producer_var)


def _extract_workflow(g: Graph, tasks_map: Dict[str, TaskModel]) -> List[WorkflowStepModel]:
    """Extract workflow steps in order."""
    steps: List[WorkflowStepModel] = []
    task_iri_to_var: Dict[str, str] = {t.iri: t.var_name for t in tasks_map.values()}
    task_iri_to_agent: Dict[str, str] = {t.iri: t.agent_iri for t in tasks_map.values()}
    edge_map: Dict[str, List[str]] = {}
    for row in g.query(STEP_EDGES_QUERY):
        source = _s(row.source)
        target = _s(row.target)
        edge_map.setdefault(source, [])
        if target not in edge_map[source]:
            edge_map[source].append(target)

    for row in g.query(WORKFLOW_QUERY):
        step_iri = _s(row.step)
        task_iri = _s(row.task)
        task_var = task_iri_to_var.get(task_iri, _safe_var(task_iri))
        order = int(row.stepOrder) if row.stepOrder is not None else len(steps) + 1
        step_type = _s(row.stepType).split("#")[-1]

        steps.append(WorkflowStepModel(
            iri=step_iri,
            var_name=_safe_var(step_iri),
            step_order=order,
            task_iri=task_iri,
            task_var_name=task_var,
            step_type=step_type,
            next_step_iris=edge_map.get(step_iri, []),
            agent_iri=task_iri_to_agent.get(task_iri, ""),
        ))

    # Sort by order
    steps.sort(key=lambda s: s.step_order)
    return steps


def _infer_workflow_type(process: ProcessType, steps: List[WorkflowStepModel]) -> WorkflowType:
    """Infer a framework-agnostic workflow topology from step edges."""
    if process == ProcessType.HIERARCHICAL:
        return WorkflowType.HIERARCHICAL
    if not steps:
        return WorkflowType.SEQUENTIAL

    step_iris = {step.iri for step in steps if step.iri}
    edges = [(step.iri, target) for step in steps for target in step.next_step_iris]
    if any(source == target or target in step_iris for source, target in edges if source == target):
        return WorkflowType.LOOP
    if any(len(step.next_step_iris) > 1 for step in steps):
        return WorkflowType.BRANCHING
    if len(edges) == 0 and len(steps) > 1:
        return WorkflowType.PARALLEL
    return WorkflowType.SEQUENTIAL


def _extract_memories(g: Graph) -> Dict[str, MemoryModel]:
    """Extract agnostic Memory individuals and raw configs."""
    memories: Dict[str, MemoryModel] = {}
    for row in g.query(MEMORY_QUERY):
        iri = _s(row.mem)
        if iri not in memories:
            memories[iri] = MemoryModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc),
                configs={},
            )

    for row in g.query(MEMORY_CONFIG_QUERY):
        iri = _s(row.mem)
        if iri in memories:
            memories[iri].configs[_s(row.key)] = _s(row.value)
    return memories


def _extract_workflow_patterns(
    g: Graph,
    steps: List[WorkflowStepModel],
    process: ProcessType,
) -> List[WorkflowPatternModel]:
    """Extract WorkflowPattern containers and attach WorkflowStep members."""
    patterns: Dict[str, WorkflowPatternModel] = {}
    step_by_iri = {step.iri: step for step in steps if step.iri}
    inferred_type = _infer_workflow_type(process, steps)

    for row in g.query(WORKFLOW_PATTERN_QUERY):
        iri = _s(row.wp)
        patterns[iri] = WorkflowPatternModel(
            iri=iri,
            var_name=_safe_var(iri),
            label=_s(row.label),
            description=_s(row.desc),
            steps=[],
            workflow_type=inferred_type,
            sub_pattern_iris=[],
        )

    for row in g.query(WORKFLOW_STEPS_QUERY):
        wp_iri = _s(row.wp)
        step_iri = _s(row.step)
        if wp_iri in patterns and step_iri in step_by_iri:
            patterns[wp_iri].steps.append(step_by_iri[step_iri])

    for row in g.query(WORKFLOW_SUB_PATTERN_QUERY):
        wp_iri = _s(row.wp)
        sub_iri = _s(row.sub)
        if wp_iri in patterns and sub_iri not in patterns[wp_iri].sub_pattern_iris:
            patterns[wp_iri].sub_pattern_iris.append(sub_iri)

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
    """Extract Team-level system configs as raw key/value strings."""
    configs: Dict[str, str] = {}
    for row in g.query(SYSTEM_CONFIG_QUERY):
        configs[_s(row.key)] = _s(row.value)
    return configs


def _extract_input_variables(
    g: Graph,
    tasks_map: Dict[str, TaskModel],
    agents_map: Dict[str, AgentModel],
) -> List[InputVariableModel]:
    """Extract all template placeholder variables from prompts and KickoffInputBundle.

    Strategy:
      1. PRIMARY: Query agento-ext:KickoffInputBundle triples (uniform, authoritative).
         If found, use these exclusively — they have key, value, and isDefault flag.
      2. FALLBACK: Legacy extraction from task descriptions + promptInputData +
         Context/Resource descriptions (for TTL files not yet migrated).
    """
    # ── Strategy 1: agento-ext:KickoffInputBundle (primary) ──
    kickoff_results = list(g.query(KICKOFF_INPUTS_QUERY))
    if kickoff_results:
        # Collect all values per key (one key may have multiple example bundles)
        key_data: Dict[str, dict] = {}  # key → {default, is_default, alternatives}
        for row in kickoff_results:
            key = _s(row.key)
            value = _s(row.value)
            is_default_str = _s(row.isDefault).lower()
            is_default = is_default_str in ("true", "1", "yes")

            if key not in key_data:
                key_data[key] = {"default": "", "is_default": False, "alternatives": []}

            if is_default and not key_data[key]["is_default"]:
                # First default wins
                key_data[key]["default"] = value
                key_data[key]["is_default"] = True
            elif value:
                key_data[key]["alternatives"].append(value)

        return [
            InputVariableModel(
                name=key,
                default_value=data["default"],
                has_default=data["is_default"] and bool(data["default"]),
                alternative_values=data["alternatives"],
            )
            for key, data in key_data.items()
        ]

    # ── Strategy 2: Legacy fallback (task descriptions + promptInputData) ──
    all_vars: Dict[str, str] = {}  # name → default_value

    # From task descriptions
    for task in tasks_map.values():
        for var_name in _extract_placeholders(task.description):
            if var_name not in all_vars:
                all_vars[var_name] = ""

    # From prompt input data
    for row in g.query(PROMPT_INPUT_DATA_QUERY):
        text = _s(row.inputData)
        for var_name in _extract_placeholders(text):
            if var_name not in all_vars:
                all_vars[var_name] = ""

    # Try to find default values from :Context / beam:Resource descriptions
    for row in g.query(DEFAULT_INPUTS_QUERY):
        desc = _s(row.desc)
        # Parse lines like "company_stock = 'AMZN'" or "- company_domain: careers.wbd.com"
        for line in desc.split("\n"):
            line = line.strip().lstrip("-").strip()
            # Match "key = value" or "key: value"
            m = re.match(r"(\w+)\s*[:=]\s*(.+)", line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip().strip("'\"")
                if key in all_vars:
                    all_vars[key] = val

    return [
        InputVariableModel(name=name, default_value=default, has_default=bool(default))
        for name, default in all_vars.items()
    ]


def _extract_env_vars(g: Graph) -> List[ConfigModel]:
    """Extract environment variable configs (API keys, etc.)."""
    env_vars: List[ConfigModel] = []
    seen: Set[str] = set()
    for row in g.query(ENV_CONFIG_QUERY):
        key = _s(row.key)
        if key not in seen:
            seen.add(key)
            env_vars.append(ConfigModel(key=key, value=_s(row.value)))
    return env_vars


# ── New extraction functions for ontology coverage ──


def _extract_goals(g: Graph) -> Dict[str, GoalModel]:
    """Extract all :Goal individuals keyed by IRI."""
    goals: Dict[str, GoalModel] = {}
    for row in g.query(GOALS_QUERY):
        iri = _s(row.goal)
        if iri not in goals:
            goals[iri] = GoalModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc),
            )
    return goals


def _extract_capabilities(g: Graph) -> Dict[str, CapabilityModel]:
    """Extract all :Capability individuals keyed by IRI."""
    caps: Dict[str, CapabilityModel] = {}
    for row in g.query(CAPABILITIES_QUERY):
        iri = _s(row.cap)
        if iri not in caps:
            caps[iri] = CapabilityModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc) or _s(row.comment) or "",
            )
    return caps


def _extract_environments(g: Graph) -> Dict[str, EnvironmentModel]:
    """Extract all :Environment individuals keyed by IRI."""
    envs: Dict[str, EnvironmentModel] = {}
    for row in g.query(ENVIRONMENTS_QUERY):
        iri = _s(row.env)
        if iri not in envs:
            envs[iri] = EnvironmentModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc),
                env_type=_s(row.envType),
            )

    for row in g.query(ENVIRONMENT_CONFIGS_QUERY):
        iri = _s(row.env)
        if iri in envs:
            envs[iri].configs[_s(row.key)] = _s(row.value)

    for row in g.query(ENVIRONMENT_CONTAINS_QUERY):
        iri = _s(row.env)
        res_iri = _s(row.resource)
        if iri in envs and res_iri not in envs[iri].contained_resource_iris:
            envs[iri].contained_resource_iris.append(res_iri)

    return envs


def _extract_objectives(g: Graph) -> Dict[str, ObjectiveModel]:
    """Extract all :Objective individuals keyed by IRI."""
    objs: Dict[str, ObjectiveModel] = {}
    for row in g.query(OBJECTIVES_QUERY):
        iri = _s(row.obj)
        if iri not in objs:
            objs[iri] = ObjectiveModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc),
                contributes_to_goal_iri=_s(row.goal),
            )
    return objs


def _extract_human_agents(g: Graph) -> Dict[str, HumanAgentModel]:
    """Extract all :HumanAgent individuals keyed by IRI."""
    humans: Dict[str, HumanAgentModel] = {}
    for row in g.query(HUMAN_AGENTS_QUERY):
        iri = _s(row.human)
        if iri not in humans:
            humans[iri] = HumanAgentModel(
                iri=iri,
                var_name=_safe_var(iri),
                role=_s(row.role),
            )

    for row in g.query(HUMAN_PARTICIPATED_QUERY):
        iri = _s(row.human)
        task_iri = _s(row.task)
        if iri in humans and task_iri not in humans[iri].participated_task_iris:
            humans[iri].participated_task_iris.append(task_iri)

    return humans


def _extract_resources(g: Graph) -> Dict[str, ResourceModel]:
    """Extract all beam:Resource (and beam:Instance) individuals keyed by IRI."""
    resources: Dict[str, ResourceModel] = {}
    for row in g.query(RESOURCES_QUERY):
        iri = _s(row.res)
        if iri not in resources:
            type_frag = _s(row.type).split("#")[-1].split("/")[-1]
            resources[iri] = ResourceModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc),
                resource_type=type_frag,
            )
    return resources


def _extract_constraints(g: Graph) -> Dict[str, ConstraintModel]:
    """Extract all :Constraint individuals keyed by IRI."""
    constraints: Dict[str, ConstraintModel] = {}
    for row in g.query(CONSTRAINTS_QUERY):
        iri = _s(row.con)
        if iri not in constraints:
            constraints[iri] = ConstraintModel(
                iri=iri,
                var_name=_safe_var(iri),
                label=_s(row.label),
                description=_s(row.desc),
            )

    for row in g.query(CONSTRAINT_CONFIGS_QUERY):
        iri = _s(row.con)
        if iri in constraints:
            constraints[iri].configs[_s(row.key)] = _s(row.value)

    return constraints


# ── Updated extraction with cross-ontology links ──


def _link_agent_relations(
    g: Graph,
    agents_map: Dict[str, AgentModel],
    tools_map: Dict[str, ToolModel],
    capabilities_map: Dict[str, CapabilityModel],
) -> None:
    """Populate agent→relationships (interactsWith, operatesIn, capabilities, objectives)."""
    for row in g.query(AGENT_INTERACTS_QUERY):
        iri = _s(row.agent)
        target = _s(row.target)
        if iri in agents_map and target not in agents_map[iri].interacts_with:
            agents_map[iri].interacts_with.append(target)

    for row in g.query(AGENT_OPERATES_IN_QUERY):
        iri = _s(row.agent)
        env_iri = _s(row.env)
        if iri in agents_map:
            agents_map[iri].operates_in_iri = env_iri

    for row in g.query(AGENT_CAPABILITY_QUERY):
        iri = _s(row.agent)
        cap_iri = _s(row.cap)
        if iri in agents_map and cap_iri not in agents_map[iri].capability_iris:
            agents_map[iri].capability_iris.append(cap_iri)

    for row in g.query(AGENT_OBJECTIVE_QUERY):
        iri = _s(row.agent)
        obj_iri = _s(row.obj)
        if iri in agents_map and obj_iri not in agents_map[iri].objective_iris:
            agents_map[iri].objective_iris.append(obj_iri)


def _link_task_relations(
    g: Graph,
    tasks_map: Dict[str, TaskModel],
) -> None:
    """Populate task→ontology relationships."""
    for row in g.query(TASK_OBJECTIVE_QUERY):
        iri = _s(row.task)
        obj_iri = _s(row.obj)
        if iri in tasks_map:
            tasks_map[iri].contributes_to_objective_iri = obj_iri

    for row in g.query(TASK_CAPABILITY_QUERY):
        iri = _s(row.task)
        cap_iri = _s(row.cap)
        if iri in tasks_map and cap_iri not in tasks_map[iri].requires_capability_iris:
            tasks_map[iri].requires_capability_iris.append(cap_iri)

    for row in g.query(TASK_PERFORMED_BY_QUERY):
        iri = _s(row.task)
        performer = _s(row.performer)
        if iri in tasks_map:
            tasks_map[iri].performed_by_iri = performer


def _link_tool_relations(
    g: Graph,
    tools_map: Dict[str, ToolModel],
    capabilities_map: Dict[str, CapabilityModel],
) -> None:
    """Populate tool→ontology relationships (capabilities, resourceUsage, toolUsage)."""
    for row in g.query(TOOL_CAPABILITY_QUERY):
        iri = _s(row.tool)
        cap_iri = _s(row.cap)
        if iri in tools_map and cap_iri not in tools_map[iri].capability_iris:
            tools_map[iri].capability_iris.append(cap_iri)
            tools_map[iri].capabilities.append(cap_iri)

    for row in g.query(TOOL_RESOURCE_USAGE_QUERY):
        iri = _s(row.tool)
        res_iri = _s(row.resource)
        if iri in tools_map and res_iri not in tools_map[iri].resource_usage_iris:
            tools_map[iri].resource_usage_iris.append(res_iri)

    for row in g.query(TOOL_TOOL_USAGE_QUERY):
        iri = _s(row.tool)
        child_iri = _s(row.child)
        if iri in tools_map and child_iri not in tools_map[iri].tool_usage_iris:
            tools_map[iri].tool_usage_iris.append(child_iri)


def _link_team_relations(
    g: Graph,
    project: AgenticProject,
    team_iri: str,
) -> None:
    """Populate team→ontology relationships on the project."""
    if not team_iri:
        return

    for row in g.query(TEAM_AGENT_MEMBERS_QUERY):
        iri = _s(row.team)
        agent_iri = _s(row.agent)
        if iri == team_iri and agent_iri not in project.agent_member_iris:
            project.agent_member_iris.append(agent_iri)

    for row in g.query(TEAM_WORKFLOW_PATTERN_QUERY):
        iri = _s(row.team)
        wp_iri = _s(row.wp)
        if iri == team_iri and wp_iri not in project.workflow_pattern_iris:
            project.workflow_pattern_iris.append(wp_iri)

    for row in g.query(TEAM_GOAL_QUERY):
        iri = _s(row.team)
        goal_iri = _s(row.goal)
        if iri == team_iri and goal_iri not in project.goal_iris:
            project.goal_iris.append(goal_iri)

    for row in g.query(TEAM_TEAM_GOAL_QUERY):
        iri = _s(row.team)
        goal_iri = _s(row.goal)
        if iri == team_iri and goal_iri not in project.goal_iris:
            project.goal_iris.append(goal_iri)

    for row in g.query(TEAM_OBJECTIVE_QUERY):
        iri = _s(row.team)
        obj_iri = _s(row.obj)
        if iri == team_iri and obj_iri not in project.objective_iris:
            project.objective_iris.append(obj_iri)


def _link_workflow_relations(
    g: Graph,
    patterns: List[WorkflowPatternModel],
) -> None:
    """Populate workflow pattern→pattern relationships."""
    pattern_by_iri = {p.iri: p for p in patterns if p.iri}

    for row in g.query(WORKFLOW_RELATED_PATTERN_QUERY):
        wp_iri = _s(row.wp)
        rel_iri = _s(row.related)
        if wp_iri in pattern_by_iri and rel_iri not in pattern_by_iri[wp_iri].related_pattern_iris:
            pattern_by_iri[wp_iri].related_pattern_iris.append(rel_iri)

    for row in g.query(WORKFLOW_NEXT_PATTERN_QUERY):
        wp_iri = _s(row.wp)
        next_iri = _s(row.next)
        if wp_iri in pattern_by_iri:
            pattern_by_iri[wp_iri].next_pattern_iri = next_iri


# ─────────────────────── Public API ───────────────────────

def extract_project(file_path: str) -> AgenticProject:
    """
    Single framework-agnostic extraction pipeline.

    KG (.ttl) → SPARQL → AgenticProject. Framework-specific generators should
    consume this through their adapter layer.
    """
    g = load_graph(file_path)

    project_name, description, process, team_iri = _extract_team(g)
    project_var_name = _safe_var(project_name)

    lm_map = _extract_language_models(g)
    tools_map = _extract_tools(g)
    memories_map = _extract_memories(g)
    agents_map = _extract_agents(g, tools_map, lm_map)
    tasks_map = _extract_tasks(g, agents_map)
    _resolve_task_context(g, tasks_map)
    workflow_steps = _extract_workflow(g, tasks_map)
    workflows = _extract_workflow_patterns(g, workflow_steps, process)

    # Full ontology coverage: extract all standalone ontology concepts
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

    if workflow_steps:
        step_order = {s.task_iri: s.step_order for s in workflow_steps}
        task_list = sorted(
            tasks_map.values(),
            key=lambda t: step_order.get(t.iri, 999),
        )
    else:
        task_list = list(tasks_map.values())

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
        input_variables=_extract_input_variables(g, tasks_map, agents_map),
        env_vars=_extract_env_vars(g),
        system_configs=_extract_system_configs(g),
        # New ontology class collections
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



