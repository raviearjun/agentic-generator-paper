"""
Layer 1 – SPARQL-based Data Extraction

Loads a CrewAI KG (.ttl) file via rdflib, runs SPARQL queries aligned
to the agentO ontology, and populates Pydantic IR models (Layer 2).

Extraction strategy:
  1. Team / Crew metadata + process type
  2. LanguageModel individuals
  3. Tool individuals (excluding LLMAgent)
  4. Agent individuals (with config fallback for role/goal/backstory)
  5. Task individuals (with prompt/config fallback for description/expected_output)
  6. Workflow ordering (WorkflowStep chain)
  7. Resource dependency → task context resolution
  8. Template variable extraction from prompt placeholders
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from rdflib import Graph

from .models import (
    AgentModel,
    ConfigModel,
    CrewProject,
    InputVariableModel,
    LanguageModelModel,
    ProcessType,
    TaskModel,
    ToolConfigModel,
    ToolModel,
    WorkflowStepModel,
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

# ── Agents ──

AGENTS_QUERY = PREFIXES + """
SELECT DISTINCT ?agent ?agentID ?role ?label
WHERE {
    ?agent a :LLMAgent .
    OPTIONAL { ?agent :agentID ?agentID }
    OPTIONAL { ?agent :agentRole ?role }
    OPTIONAL { ?agent rdfs:label ?label }
}
"""

AGENT_GOAL_FROM_GOAL_QUERY = PREFIXES + """
SELECT ?agent ?goalDesc
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentGoal ?goal .
    ?goal dcterms:description ?goalDesc .
}
"""

AGENT_CONFIG_QUERY = PREFIXES + """
SELECT ?agent ?key ?value
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentConfig ?cfg .
    ?cfg :configKey ?key ;
         :configValue ?value .
}
"""

AGENT_BACKSTORY_FROM_PROMPT_QUERY = PREFIXES + """
SELECT ?agent ?instruction
WHERE {
    ?agent a :LLMAgent ;
           :agentPrompt ?prompt .
    ?prompt :promptInstruction ?instruction .
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

AGENT_DELEGATION_QUERY = PREFIXES + """
SELECT ?agent ?value
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentConfig ?cfg .
    ?cfg :configKey "allow_delegation" ;
         :configValue ?value .
}
"""

AGENT_VERBOSE_QUERY = PREFIXES + """
SELECT ?agent ?value
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentConfig ?cfg .
    ?cfg :configKey "verbose" ;
         :configValue ?value .
}
"""

# Fallback: extract delegation/verbose from description, comment, prompt text
AGENT_TEXT_FIELDS_QUERY = PREFIXES + """
SELECT ?agent ?desc ?comment ?promptCtx ?promptInstr
WHERE {
    ?agent a :LLMAgent .
    OPTIONAL { ?agent dcterms:description ?desc }
    OPTIONAL { ?agent rdfs:comment ?comment }
    OPTIONAL {
        ?agent :agentPrompt ?prompt .
        OPTIONAL { ?prompt :promptContext ?promptCtx }
        OPTIONAL { ?prompt :promptInstruction ?promptInstr }
    }
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
SELECT ?task ?instruction ?outputIndicator
WHERE {
    ?task a :Task .
    {
        { ?task :taskPrompt ?prompt }
        UNION
        { ?task :hasPrompt ?prompt }
    }
    ?prompt a :Prompt .
    OPTIONAL { ?prompt :promptInstruction ?instruction }
    OPTIONAL { ?prompt :promptOutputIndicator ?outputIndicator }
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

# ── Input Variables (from prompt input data) ──

PROMPT_INPUT_DATA_QUERY = PREFIXES + """
SELECT DISTINCT ?inputData
WHERE {
    ?prompt a :Prompt ;
            :promptInputData ?inputData .
}
"""

# ── Default inputs (from :Context / beam:Resource) ──

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


def _parse_bool_from_text(text: str, key: str) -> Optional[bool]:
    """
    Extract a boolean flag from free text using multiple patterns.

    Recognizes:
        allow_delegation=False
        allow_delegation: False
        AllowDelegation: False
        allow_delegation = True
        verbose=True
        verbose: 2  (truthy)
    """
    if not text:
        return None
    # Normalize key variants (e.g. AllowDelegation -> allow_delegation)
    key_pattern = re.escape(key)
    # Also match CamelCase variant: allow_delegation -> AllowDelegation
    camel_variant = "".join(w.capitalize() for w in key.split("_"))
    camel_pattern = re.escape(camel_variant)
    pattern = rf"(?:{key_pattern}|{camel_pattern})\s*[:=]\s*(\S+)"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        val = m.group(1).strip().strip("'\",;.")
        if val.lower() in ("false", "0", "no", "none"):
            return False
        if val.lower() in ("true", "1", "yes") or val.isdigit():
            return True
    return None


# ── Strategy 1.5 helpers: raw TTL parsing for Config KV pairs ──

AGENT_CONFIG_LINK_QUERY = PREFIXES + """
SELECT ?agent ?cfg
WHERE {
    ?agent a :LLMAgent ;
           :hasAgentConfig ?cfg .
}
"""


def _parse_config_kv_from_ttl(raw_ttl: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    Parse raw Turtle text to extract ordered configKey→configValue pairs
    per Config node.  This recovers the pairing that SPARQL loses due to
    the cartesian product on multi-KV Config nodes.

    Uses a position-based approach: find all Config declarations and all
    KV pairs in the file, then associate each KV pair with the nearest
    preceding Config node.

    Returns {config_local_name: [(key, value), ...]}
    """
    result: Dict[str, List[Tuple[str, str]]] = {}

    # Find Config node declarations and their positions
    config_decl_pattern = re.compile(r':(\S+)\s+a\s+:Config\b')
    config_positions: List[Tuple[int, str]] = []  # (pos, local_name)
    for m in config_decl_pattern.finditer(raw_ttl):
        config_positions.append((m.start(), m.group(1)))

    if not config_positions:
        return result

    # Find all KV pairs and their positions
    kv_pattern = re.compile(
        r':configKey\s+"([^"]*?)"\s*;\s*:configValue\s+"((?:[^"\\]|\\.)*)"\s*',
    )
    for kv_m in kv_pattern.finditer(raw_ttl):
        kv_pos = kv_m.start()
        key, value = kv_m.group(1), kv_m.group(2)
        # Find the nearest preceding Config node
        owner = None
        for cfg_pos, cfg_local in reversed(config_positions):
            if cfg_pos <= kv_pos:
                owner = cfg_local
                break
        if owner:
            result.setdefault(owner, []).append((key, value))

    return result


def _find_config_value_for_agent(
    g: Graph,
    agent_iri: str,
    target_key: str,
    ttl_kv: Dict[str, List[Tuple[str, str]]],
) -> Optional[str]:
    """
    Find the configValue paired with *target_key* for a specific agent,
    using the raw-TTL-parsed KV pairs to get the correct pairing.
    """
    # Get all Config IRIs linked to this agent
    for row in g.query(AGENT_CONFIG_LINK_QUERY):
        a_iri = _s(row.agent)
        if a_iri != agent_iri:
            continue
        cfg_iri = _s(row.cfg)
        # Extract local name from the full IRI (after # or last /)
        cfg_local = cfg_iri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
        if cfg_local in ttl_kv:
            for kv_key, kv_val in ttl_kv[cfg_local]:
                if kv_key == target_key:
                    return kv_val
    return None


def _extract_team(g: Graph) -> Tuple[str, str, ProcessType]:
    """Extract team name, description, and process type."""
    crew_name = "MyCrew"
    description = ""
    process = ProcessType.SEQUENTIAL

    results = list(g.query(TEAM_QUERY))
    if results:
        row = results[0]
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

    return crew_name, description, process


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
    raw_ttl: str = "",
) -> Dict[str, AgentModel]:
    """Extract LLMAgent individuals with full property resolution."""
    agents: Dict[str, AgentModel] = {}

    # Primary properties
    for row in g.query(AGENTS_QUERY):
        iri = _s(row.agent)
        if iri in agents:
            continue
        agent_id = _s(row.agentID)
        label = _s(row.label)
        role = _s(row.role)

        # Determine var_name: prefer agentID or label
        var_name = agent_id or label or _safe_var(iri)
        var_name = _safe_var(var_name) if not re.match(r'^[a-z_][a-z0-9_]*$', var_name) else var_name

        agents[iri] = AgentModel(
            iri=iri,
            var_name=var_name,
            agent_id=agent_id,
            role=role,
            goal="",
            backstory="",
            tool_var_names=[],
            llm=None,
            allow_delegation=None,
        )

    # Goal from :hasAgentGoal → Goal → dcterms:description
    for row in g.query(AGENT_GOAL_FROM_GOAL_QUERY):
        iri = _s(row.agent)
        if iri in agents and not agents[iri].goal:
            agents[iri].goal = _s(row.goalDesc)

    # Config fallback for role/goal/backstory
    for row in g.query(AGENT_CONFIG_QUERY):
        iri = _s(row.agent)
        if iri not in agents:
            continue
        key = _s(row.key).lower()
        value = _s(row.value)
        if key == "goal" and not agents[iri].goal:
            agents[iri].goal = value
        elif key == "backstory" and not agents[iri].backstory:
            agents[iri].backstory = value
        elif key == "role" and not agents[iri].role:
            agents[iri].role = value

    # Backstory from prompt
    for row in g.query(AGENT_BACKSTORY_FROM_PROMPT_QUERY):
        iri = _s(row.agent)
        if iri in agents and not agents[iri].backstory:
            agents[iri].backstory = _s(row.instruction)

    # Agent → Tool links
    for row in g.query(AGENT_TOOLS_QUERY):
        iri = _s(row.agent)
        tool_iri = _s(row.tool)
        if iri in agents and tool_iri in tools_map:
            tool_var = tools_map[tool_iri].var_name
            if tool_var not in agents[iri].tool_var_names:
                agents[iri].tool_var_names.append(tool_var)

    # Agent → LanguageModel
    for row in g.query(AGENT_LLM_QUERY):
        iri = _s(row.agent)
        lm_iri = _s(row.lm)
        if iri in agents and lm_iri in lm_map:
            agents[iri].llm = lm_map[lm_iri]

    # allow_delegation config (Strategy 1: explicit configKey)
    # Collect boolean-like values per agent first to handle cartesian products
    # from multi-KV Config nodes (same node has role, goal, backstory, etc.)
    _deleg_bools: Dict[str, Set[bool]] = {}
    for row in g.query(AGENT_DELEGATION_QUERY):
        iri = _s(row.agent)
        if iri not in agents:
            continue
        val = _s(row.value).strip().lower()
        if val in ("true", "false", "0", "1", "yes", "no"):
            _deleg_bools.setdefault(iri, set()).add(val in ("true", "1", "yes"))
    for iri, bools in _deleg_bools.items():
        if len(bools) == 1:  # unambiguous — only one distinct boolean value
            agents[iri].allow_delegation = bools.pop()
        # else: ambiguous (both True & False found from cartesian product) → skip

    # verbose config (Strategy 1: explicit configKey)
    _verbose_bools: Dict[str, Set[bool]] = {}
    for row in g.query(AGENT_VERBOSE_QUERY):
        iri = _s(row.agent)
        if iri not in agents:
            continue
        val = _s(row.value).strip().lower()
        if val in ("true", "false", "0", "1", "yes", "no", "none") or val.isdigit():
            if val in ("false", "0", "no", "none"):
                _verbose_bools.setdefault(iri, set()).add(False)
            else:
                _verbose_bools.setdefault(iri, set()).add(True)
    for iri, bools in _verbose_bools.items():
        if len(bools) == 1:  # unambiguous
            agents[iri].verbose = bools.pop()
        # else: ambiguous → skip, let Strategy 2 handle it

    # Strategy 1.5: parse raw TTL text to recover key→value pairing
    # RDF loses configKey→configValue pairing on multi-KV nodes, but the
    # original Turtle syntax keeps them adjacent:
    #   :configKey "allow_delegation" ; :configValue "False" ;
    # We use regex on the raw file to extract the actual pairs.
    if raw_ttl:
        _ttl_kv = _parse_config_kv_from_ttl(raw_ttl)
        for iri, agent in agents.items():
            if agent.allow_delegation is None:
                _found_deleg = _find_config_value_for_agent(
                    g, iri, "allow_delegation", _ttl_kv
                )
                if _found_deleg is not None:
                    agent.allow_delegation = _found_deleg.lower() in ("true", "1", "yes")
            if agent.verbose is None:
                _found_verbose = _find_config_value_for_agent(
                    g, iri, "verbose", _ttl_kv
                )
                if _found_verbose is not None:
                    val = _found_verbose.lower()
                    agent.verbose = val not in ("false", "0", "no", "none")

    # Strategy 2: extract delegation + verbose from text fields
    # (dcterms:description, rdfs:comment, promptContext, promptInstruction)
    for row in g.query(AGENT_TEXT_FIELDS_QUERY):
        iri = _s(row.agent)
        if iri not in agents:
            continue
        agent = agents[iri]
        # Concatenate all text fields for this agent
        all_text = " ".join(filter(None, [
            _s(row.desc), _s(row.comment),
            _s(row.promptCtx), _s(row.promptInstr),
        ]))
        if not all_text.strip():
            continue
        # Only fill if Strategy 1 didn't find a value
        if agent.allow_delegation is None:
            parsed = _parse_bool_from_text(all_text, "allow_delegation")
            if parsed is not None:
                agent.allow_delegation = parsed
        if agent.verbose is None:
            parsed = _parse_bool_from_text(all_text, "verbose")
            if parsed is not None:
                agent.verbose = parsed

    # Final defaults
    for agent in agents.values():
        if not agent.role:
            agent.role = "LLM Agent"
        if not agent.goal:
            agent.goal = agent.role
        if not agent.backstory:
            agent.backstory = f"You are a {agent.role}."

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
            description=desc,
            expected_output="",
            agent_var_name=agent_iri_to_var.get(agent_iri, ""),
            context_task_var_names=[],
        )

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
        output = _s(row.outputIndicator)
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
            resource_to_producer[res_iri] = tasks_map[task_iri].var_name

    # For each task's required resources, find the producing task
    for row in g.query(TASK_REQUIRES_QUERY):
        task_iri = _s(row.task)
        res_iri = _s(row.resource)
        if task_iri in tasks_map and res_iri in resource_to_producer:
            producer_var = resource_to_producer[res_iri]
            task = tasks_map[task_iri]
            if producer_var != task.var_name and producer_var not in task.context_task_var_names:
                task.context_task_var_names.append(producer_var)


def _extract_workflow(g: Graph, tasks_map: Dict[str, TaskModel]) -> List[WorkflowStepModel]:
    """Extract workflow steps in order."""
    steps: List[WorkflowStepModel] = []
    task_iri_to_var: Dict[str, str] = {t.iri: t.var_name for t in tasks_map.values()}

    for row in g.query(WORKFLOW_QUERY):
        task_iri = _s(row.task)
        task_var = task_iri_to_var.get(task_iri, _safe_var(task_iri))
        order = int(row.stepOrder) if row.stepOrder is not None else len(steps) + 1
        step_type = _s(row.stepType).split("#")[-1]

        steps.append(WorkflowStepModel(
            step_order=order,
            task_var_name=task_var,
            step_type=step_type,
        ))

    # Sort by order
    steps.sort(key=lambda s: s.step_order)
    return steps


def _extract_input_variables(
    g: Graph,
    tasks_map: Dict[str, TaskModel],
    agents_map: Dict[str, AgentModel],
) -> List[InputVariableModel]:
    """Extract all template placeholder variables from prompts and descriptions."""
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
        InputVariableModel(name=name, default_value=default)
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


# ─────────────────────── Public API ───────────────────────

def extract_crew_project(file_path: str) -> CrewProject:
    """
    Full SPARQL extraction pipeline for a single KG file.

    Returns a complete CrewProject Pydantic model ready for Layer 3.
    """
    g = load_graph(file_path)

    # Read raw TTL text for Strategy 1.5 (Config KV pair recovery)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_ttl = f.read()
    except Exception:
        raw_ttl = ""

    # 1. Team metadata
    crew_name, description, process = _extract_team(g)
    crew_var_name = _safe_var(crew_name)

    # 2. Language models
    lm_map = _extract_language_models(g)

    # 3. Tools
    tools_map = _extract_tools(g)

    # 4. Agents
    agents_map = _extract_agents(g, tools_map, lm_map, raw_ttl)

    # 5. Tasks
    tasks_map = _extract_tasks(g, agents_map)

    # 6. Task context resolution
    _resolve_task_context(g, tasks_map)

    # 7. Workflow ordering
    workflow_steps = _extract_workflow(g, tasks_map)

    # 8. Reorder tasks by workflow
    if workflow_steps:
        step_order = {s.task_var_name: s.step_order for s in workflow_steps}
        task_list = sorted(
            tasks_map.values(),
            key=lambda t: step_order.get(t.var_name, 999),
        )
    else:
        task_list = list(tasks_map.values())

    # 9. Input variables
    input_variables = _extract_input_variables(g, tasks_map, agents_map)

    # 10. Env vars
    env_vars = _extract_env_vars(g)

    project = CrewProject(
        crew_name=crew_name,
        crew_var_name=crew_var_name,
        description=description,
        process=process,
        agents=list(agents_map.values()),
        tasks=task_list,
        tools=list(tools_map.values()),
        workflow_steps=workflow_steps,
        input_variables=input_variables,
        language_models=list(lm_map.values()),
        env_vars=env_vars,
    )

    print(
        f"  [Extracted] crew={crew_name}, "
        f"{len(project.agents)} agents, "
        f"{len(project.tasks)} tasks, "
        f"{len(project.tools)} tools, "
        f"{len(project.workflow_steps)} workflow steps"
    )

    return project
