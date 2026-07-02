"""SPARQL query constants for the agentO ontology extraction pipeline.

All queries operate against the canonical ontology namespace:
  http://www.w3id.org/agentic-ai/onto#

Queries are grouped by the ontology class they interrogate.
"""

from __future__ import annotations

# ─────────────────────── Namespace Prefixes ───────────────────────

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
    OPTIONAL { ?team dcterms:title ?title }
    OPTIONAL { ?team dcterms:description ?desc }
    BIND(COALESCE(?label, ?title) AS ?label)
}
"""

# (Orchestration/process info will be retrieved generically via system config key "process")

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
# Single consolidated query extracts all single-valued scalar properties in one pass.
# Multi-valued relations (tools, LLM) use separate queries.

AGENTS_QUERY = PREFIXES + """
SELECT DISTINCT ?agent ?agentID ?role ?label ?goal ?goalDesc ?backstory
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

# (Task description and expected output will be retrieved generically via task config keys "description" and "expected_output")

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
    OPTIONAL {
        ?step a ?stepType .
        FILTER(?stepType IN (:WorkflowStep, :StartStep, :EndStep))
    }
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
SELECT DISTINCT ?source ?target
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

# ── Constraints ──

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
