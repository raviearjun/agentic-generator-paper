"""Canonical IR models for the agentO extraction pipeline.

This module is strictly framework-agnostic. Every model here maps directly to
an ontology class or property, with no framework-specific fields or terminology.

Framework adapters (crewai/, autogen/, langgraph/, mastra/) are responsible for
deriving their own framework-specific fields from these models.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class WorkflowType(str, Enum):
    """Framework-agnostic workflow topology inferred from agentO workflow data."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    BRANCHING = "branching"
    HIERARCHICAL = "hierarchical"
    LOOP = "loop"
    MIXED = "mixed"


# ──────────────────────────────────────────────
# Leaf Models
# ──────────────────────────────────────────────

class ConfigModel(BaseModel):
    """A single key-value configuration entry from KG :Config."""
    key: str = Field(..., description="Config key (e.g. 'api_key', 'process')")
    value: str = Field(..., description="Config value")


class GoalModel(BaseModel):
    """agentO :Goal individual — agent or team objective."""
    iri: str = Field(..., description="Full IRI of the Goal individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")


class CapabilityModel(BaseModel):
    """agentO :Capability individual — a thing an agent or tool can do."""
    iri: str = Field(..., description="Full IRI of the Capability individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="rdfs:comment / dcterms:description")


class EnvironmentModel(BaseModel):
    """agentO :Environment individual — operational context for agents."""
    iri: str = Field(..., description="Full IRI of the Environment individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    env_type: str = Field("", description=":envType literal (e.g. 'virtual', 'physical')")
    configs: Dict[str, str] = Field(default_factory=dict, description=":hasEnvironmentConfig key/value pairs")
    contained_resource_iris: List[str] = Field(default_factory=list, description=":containsResource targets")


class ObjectiveModel(BaseModel):
    """agentO :Objective individual — sub-goal contributing to a higher :Goal."""
    iri: str = Field(..., description="Full IRI of the Objective individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    contributes_to_goal_iri: str = Field("", description=":contributesToGoal target IRI")


class HumanAgentModel(BaseModel):
    """agentO :HumanAgent individual — human-in-the-loop participant."""
    iri: str = Field(..., description="Full IRI of the HumanAgent individual")
    var_name: str = Field("", description="Snake-case identifier")
    role: str = Field("", description=":agentRole literal")
    participated_task_iris: List[str] = Field(default_factory=list, description=":humanParticipatedIn targets")


class ResourceModel(BaseModel):
    """beam:Resource individual (or subclass beam:Instance)."""
    iri: str = Field(..., description="Full IRI of the Resource individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    resource_type: str = Field("", description="Type fragment e.g. 'Resource', 'Instance'")


class ConstraintModel(BaseModel):
    """agentO :Constraint individual — a rule or condition defined in the KG."""
    iri: str = Field(..., description="Full IRI of the Constraint individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    configs: Dict[str, str] = Field(default_factory=dict)


class LanguageModelModel(BaseModel):
    """agentO :LanguageModel individual — LLM backing one or more agents."""
    iri: str = Field(..., description="Full IRI of the LanguageModel individual")
    name: str = Field("", description="Human-readable name / rdfs:label")
    description: str = Field("", description="dcterms:description text")
    provider: str = Field("", description="Provider identifier if asserted in KG (e.g. 'openai', 'ollama')")
    model_name: str = Field("", description="Model identifier if asserted in KG (e.g. 'gpt-4o', 'llama3.1')")


class ToolConfigModel(BaseModel):
    """Tool-specific configuration entry from :hasToolConfig."""
    key: str = Field(..., description="Config key (e.g. 'file_path', 'stock_name')")
    value: str = Field(..., description="Config value")


class ToolModel(BaseModel):
    """agentO :Tool individual (excludes :LLMAgent which is a :Tool subclass)."""
    iri: str = Field(..., description="Full IRI of the Tool individual")
    var_name: str = Field(..., description="Snake-case identifier derived from IRI fragment")
    label: str = Field("", description="rdfs:label or display name")
    description: str = Field("", description="Tool description (dcterms:description or rdfs:comment)")
    configs: List[ToolConfigModel] = Field(default_factory=list, description=":hasToolConfig entries")
    capability_iris: List[str] = Field(default_factory=list, description=":hasCapability target IRIs")
    resource_usage_iris: List[str] = Field(default_factory=list, description=":resourceUsage target IRIs")
    tool_usage_iris: List[str] = Field(default_factory=list, description=":toolUsage child tool IRIs")


# ──────────────────────────────────────────────
# Agent Model
# ──────────────────────────────────────────────

class AgentModel(BaseModel):
    """agentO :LLMAgent individual — an AI agent defined in the knowledge graph.

    Fields map directly to ontology properties. Framework-specific derived fields
    (e.g. CrewAI allow_delegation, AutoGen is_termination_agent) are the
    responsibility of each framework's adapter layer.
    """
    iri: str = Field(..., description="Full IRI of the LLMAgent individual")
    var_name: str = Field(..., description="Snake-case identifier derived from :agentID or rdfs:label")
    agent_id: str = Field("", description=":agentID literal")

    # Core ontology fields
    role: str = Field("", description=":agentRole literal")
    goal: str = Field("", description="Goal description text (via :hasAgentGoal → :Goal → dcterms:description)")
    goal_iri: str = Field("", description="IRI of the :Goal individual linked via :hasAgentGoal")
    backstory: str = Field("", description="System prompt context (via :agentPrompt → :Prompt → :promptContext)")
    system_prompt: str = Field("", description="Same as backstory — canonical name for the agent's prompt context")

    # Relationships to other ontology individuals
    tool_iris: List[str] = Field(default_factory=list, description=":agentToolUsage target Tool IRIs")
    language_model: Optional[LanguageModelModel] = Field(None, description=":useLanguageModel target")
    knowledge_iris: List[str] = Field(default_factory=list, description=":hasKnowledge target IRIs")
    interacts_with: List[str] = Field(default_factory=list, description=":interactsWith target agent IRIs")
    operates_in_iri: str = Field("", description=":operatesIn target Environment IRI")
    capability_iris: List[str] = Field(default_factory=list, description=":hasAgentCapability target Capability IRIs")
    objective_iris: List[str] = Field(default_factory=list, description=":hasObjective target Objective IRIs")

    # Raw config bag — framework adapters read framework-specific keys from here
    configs: Dict[str, str] = Field(default_factory=dict, description="All :hasAgentConfig key/value pairs")


# ──────────────────────────────────────────────
# Task Model
# ──────────────────────────────────────────────

class TaskModel(BaseModel):
    """agentO :Task individual — a unit of work performed by an agent.

    Fields map directly to ontology properties. Framework-specific derived
    fields are the responsibility of each framework's adapter layer.
    """
    iri: str = Field(..., description="Full IRI of the Task individual")
    var_name: str = Field(..., description="Snake-case identifier derived from rdfs:label")
    label: str = Field("", description="rdfs:label")

    # Core task content
    description: str = Field("", description="Task description (may contain {placeholders})")
    expected_output: str = Field("", description="Expected output description (derived/fallback field for framework compatibility)")

    # Prompt fields (from :Prompt individual linked via :taskPrompt or :hasPrompt)
    prompt_instruction: str = Field("", description=":promptInstruction literal")
    prompt_input_data: str = Field("", description=":promptInputData literal")
    prompt_output_indicator: str = Field("", description=":promptOutputIndicator literal")
    prompt_context: str = Field("", description=":promptContext literal")

    # Agent assignment
    agent_iri: str = Field("", description=":performedByAgent target IRI")
    agent_var_name: str = Field("", description="Resolved agent snake-case identifier")

    # Resource dependency chain (from :producedResource / :requiresResource)
    context_task_var_names: List[str] = Field(
        default_factory=list,
        description="var_names of tasks whose produced resources this task requires"
    )
    produced_resources: List[str] = Field(default_factory=list, description=":producedResource target IRIs")
    required_resources: List[str] = Field(default_factory=list, description=":requiresResource target IRIs")

    # Ontology relationship fields
    contributes_to_objective_iri: str = Field("", description=":contributesToObjective target IRI")
    requires_capability_iris: List[str] = Field(default_factory=list, description=":requiresCapability target IRIs")
    performed_by_iri: str = Field("", description=":performedBy target IRI (non-LLMAgent performers)")

    # Human-in-the-loop flag — computed from HumanAgent.participated_task_iris
    human_input: bool = Field(False, description="True if a :HumanAgent participates via :humanParticipatedIn")

    # Raw config bag — framework adapters read framework-specific keys from here
    configs: Dict[str, str] = Field(default_factory=dict, description="All :hasAgentConfig key/value pairs")


# ──────────────────────────────────────────────
# Workflow Step Model
# ──────────────────────────────────────────────

class WorkflowStepModel(BaseModel):
    """agentO :WorkflowStep individual — one step in a workflow sequence."""
    iri: str = Field("", description="Full IRI of the WorkflowStep individual")
    var_name: str = Field("", description="Snake-case identifier")
    step_order: int = Field(..., description="Integer step order (:stepOrder literal)")
    task_iri: str = Field("", description=":hasAssociatedTask target IRI")
    task_var_name: str = Field(..., description="Associated task snake-case identifier")
    step_type: str = Field("WorkflowStep", description="Type fragment: StartStep / WorkflowStep / EndStep")
    next_step_iris: List[str] = Field(default_factory=list, description=":nextStep target IRIs")
    agent_iri: str = Field("", description="Agent IRI resolved from the associated task")
    description: str = Field("", description="Step description")


class WorkflowPatternModel(BaseModel):
    """agentO :WorkflowPattern — a named workflow topology with ordered steps."""
    iri: str
    var_name: str
    label: str = ""
    description: str = ""
    steps: List[WorkflowStepModel] = Field(default_factory=list)
    workflow_type: WorkflowType = WorkflowType.SEQUENTIAL
    sub_pattern_iris: List[str] = Field(default_factory=list, description=":hasSubPattern targets")
    related_pattern_iris: List[str] = Field(default_factory=list, description=":hasRelatedPattern targets (non-sub)")
    next_pattern_iri: str = Field("", description=":nextPattern target IRI")


class MemoryModel(BaseModel):
    """agentO :Memory individual — memory store available to agents."""
    iri: str
    var_name: str
    label: str = ""
    description: str = ""
    configs: Dict[str, str] = Field(default_factory=dict, description=":hasConfig key/value pairs")


# ──────────────────────────────────────────────
# Top-level Project Model
# ──────────────────────────────────────────────

class AgenticProject(BaseModel):
    """Framework-agnostic extraction result from a single KG file.

    Produced by extract_project() and consumed by framework adapters.
    All collections are keyed by IRI in the extractor and flattened to lists here.
    """
    name: str
    var_name: str = ""
    description: str = ""
    team_iri: str = Field("", description="IRI of the :Team individual")

    # Team relationship targets (IRIs only — resolve via the collections below)
    agent_member_iris: List[str] = Field(default_factory=list, description=":hasAgentMember targets")
    workflow_pattern_iris: List[str] = Field(default_factory=list, description=":hasWorkflowPattern targets")
    goal_iris: List[str] = Field(default_factory=list, description="Team-level :hasGoal / :hasTeamGoal targets")
    objective_iris: List[str] = Field(default_factory=list, description="Team-level :hasObjective targets")

    # Core ontology class collections
    agents: List[AgentModel] = Field(default_factory=list)
    tasks: List[TaskModel] = Field(default_factory=list)
    tools: List[ToolModel] = Field(default_factory=list)
    workflows: List[WorkflowPatternModel] = Field(default_factory=list)
    memories: List[MemoryModel] = Field(default_factory=list)
    language_models: List[LanguageModelModel] = Field(default_factory=list)

    # Supporting ontology class collections
    goals: List[GoalModel] = Field(default_factory=list)
    capabilities: List[CapabilityModel] = Field(default_factory=list)
    environments: List[EnvironmentModel] = Field(default_factory=list)
    objectives: List[ObjectiveModel] = Field(default_factory=list)
    human_agents: List[HumanAgentModel] = Field(default_factory=list)
    resources: List[ResourceModel] = Field(default_factory=list)
    constraints: List[ConstraintModel] = Field(default_factory=list)

    # Runtime configuration
    env_vars: List[ConfigModel] = Field(default_factory=list)
    system_configs: Dict[str, str] = Field(default_factory=dict)
