"""Layer 2 canonical IR models.

This module is framework-agnostic and defines ontology-centered models used by
the extractor and adapters. Framework-specific project IR models live under
their respective framework packages.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class ProcessType(str, Enum):
    """CrewAI Process type."""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"


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
    key: str = Field(..., description="Config key (e.g. 'role', 'api_key', 'process')")
    value: str = Field(..., description="Config value")


class GoalModel(BaseModel):
    """agentO :Goal individual — agent or team objective."""
    iri: str = Field(..., description="Full IRI of the Goal individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")


class CapabilityModel(BaseModel):
    """agentO :Capability individual — a thing an agent/tool can do."""
    iri: str = Field(..., description="Full IRI of the Capability individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="rdfs:comment / description")


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
    """agentO :Objective individual — sub-goal contributing to a higher Goal."""
    iri: str = Field(..., description="Full IRI of the Objective individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    contributes_to_goal_iri: str = Field("", description=":contributesToGoal target IRI")


class HumanAgentModel(BaseModel):
    """agentO :HumanAgent individual — human-in-the-loop."""
    iri: str = Field(..., description="Full IRI of the HumanAgent individual")
    var_name: str = Field("", description="Snake-case identifier")
    role: str = Field("", description="Human role / description")
    participated_task_iris: List[str] = Field(default_factory=list, description=":humanParticipatedIn targets")


class ResourceModel(BaseModel):
    """beam:Resource individual (or subclass :Instance / :Model)."""
    iri: str = Field(..., description="Full IRI of the Resource individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    resource_type: str = Field("", description="Type fragment e.g. 'Resource', 'Instance', 'Model'")


class ConstraintModel(BaseModel):
    """agentO :Constraint individual — a rule/condition derived from KB."""
    iri: str = Field(..., description="Full IRI of the Constraint individual")
    var_name: str = Field("", description="Snake-case identifier")
    label: str = Field("", description="rdfs:label")
    description: str = Field("", description="dcterms:description")
    configs: Dict[str, str] = Field(default_factory=dict)


class LanguageModelModel(BaseModel):
    """Represents a KG :LanguageModel (LLM backing agents)."""
    iri: str = Field(..., description="Full IRI of the LanguageModel individual")
    name: str = Field("", description="Human-readable name / label")
    description: str = Field("", description="dcterms:description text")
    provider: str = Field("", description="Inferred provider (e.g. 'ollama', 'openai')")
    model_name: str = Field("", description="Model identifier (e.g. 'llama3.1', 'gpt-4o')")


class ToolConfigModel(BaseModel):
    """Tool-specific configuration entry."""
    key: str = Field(..., description="Config key (e.g. 'file_path', 'stock_name')")
    value: str = Field(..., description="Config value")


class ToolModel(BaseModel):
    """
    Represents a standalone KG :Tool (not LLMAgent).

    Maps to:
      - crew.py: tool import + instantiation at module level
      - agents.yaml: referenced in agent's tools list
    """
    iri: str = Field(..., description="Full IRI of the Tool individual")
    var_name: str = Field(..., description="Python variable name (snake_case)")
    label: str = Field("", description="rdfs:label or display name")
    class_name: str = Field("", description="Legacy inferred CrewAI tool class")
    description: str = Field("", description="Tool description")
    configs: List[ToolConfigModel] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list, description="Legacy stub — use capability_iris")
    capability_iris: List[str] = Field(default_factory=list, description="IRI refs to :Capability individuals (via :hasCapability)")
    resource_usage_iris: List[str] = Field(default_factory=list, description="IRI refs to beam:Resource (via :resourceUsage)")
    tool_usage_iris: List[str] = Field(default_factory=list, description="IRI refs to :Tool children (via :toolUsage)")


# ──────────────────────────────────────────────
# Agent Model
# ──────────────────────────────────────────────

class AgentModel(BaseModel):
    """
    Represents a KG :LLMAgent → CrewAI Agent.

    agents.yaml fields : role, goal, backstory
    crew.py fields     : tools, llm, allow_delegation, verbose
    """
    iri: str = Field(..., description="Full IRI")
    var_name: str = Field(..., description="Python method/variable name (snake_case)")
    agent_id: str = Field("", description=":agentID literal")

    # agents.yaml fields
    role: str = Field(..., description="Agent role")
    goal: str = Field(..., description="Agent goal (text description)")
    goal_iri: str = Field("", description="IRI of the :Goal individual linked via :hasAgentGoal")
    backstory: str = Field("", description="Legacy CrewAI backstory / system prompt")
    system_prompt: str = Field("", description="agentO Prompt context/instruction")
    interacts_with: List[str] = Field(default_factory=list, description="IRI refs to other :LLMAgent individuals (via :interactsWith)")

    # crew.py fields
    tool_iris: List[str] = Field(default_factory=list, description="Tool IRI references")
    tool_var_names: List[str] = Field(default_factory=list, description="Legacy tool variable names")
    language_model: Optional[LanguageModelModel] = Field(None, description="Agnostic language model reference")
    llm: Optional[LanguageModelModel] = Field(None, description="Language model if not default")
    configs: Dict[str, str] = Field(default_factory=dict, description="All agent config key/value pairs")
    knowledge_iris: List[str] = Field(default_factory=list, description="Knowledge / memory IRI references")
    allow_delegation: Optional[bool] = Field(None, description="Allow delegation flag")
    verbose: Optional[bool] = Field(None, description="Verbose flag (None = not specified in KG → omit from output)")

    # Ontology-linked fields
    operates_in_iri: str = Field("", description=":operatesIn target Environment IRI")
    capability_iris: List[str] = Field(default_factory=list, description=":hasAgentCapability target Capability IRIs")
    objective_iris: List[str] = Field(default_factory=list, description=":hasObjective target Objective IRIs")


# ──────────────────────────────────────────────
# Task Model
# ──────────────────────────────────────────────

class TaskModel(BaseModel):
    """
    Represents a KG :Task → CrewAI Task.

    tasks.yaml fields : description, expected_output
    crew.py fields    : agent, context, output_json, output_file
    """
    iri: str = Field(..., description="Full IRI")
    var_name: str = Field(..., description="Python method/variable name (snake_case)")
    label: str = Field("", description="rdfs:label")

    # tasks.yaml fields
    description: str = Field(..., description="Task description (may contain {placeholders})")
    expected_output: str = Field(..., description="Expected output description")
    prompt_instruction: str = Field("", description="agentO promptInstruction")
    prompt_input_data: str = Field("", description="agentO promptInputData")
    prompt_output_indicator: str = Field("", description="agentO promptOutputIndicator")
    prompt_context: str = Field("", description="agentO promptContext")

    # crew.py fields
    agent_iri: str = Field("", description="Agent IRI from :performedByAgent")
    agent_var_name: str = Field("", description="Assigned agent's var_name")
    context_task_var_names: List[str] = Field(
        default_factory=list,
        description="Prior task var_names this task depends on (requiresResource chain)"
    )
    output_json_model: Optional[str] = Field(
        None,
        description="Pydantic model name for structured JSON output"
    )
    produced_resources: List[str] = Field(default_factory=list)
    required_resources: List[str] = Field(default_factory=list)
    configs: Dict[str, str] = Field(default_factory=dict)

    # Ontology-linked fields
    contributes_to_objective_iri: str = Field("", description=":contributesToObjective target IRI")
    requires_capability_iris: List[str] = Field(default_factory=list, description=":requiresCapability target Capability IRIs")
    performed_by_iri: str = Field("", description=":performedBy target Tool/Agent IRI (parent of :performedByAgent)")
    human_input: bool = Field(False, description="True if a HumanAgent participates in this task via :humanParticipatedIn")


# ──────────────────────────────────────────────
# Workflow Step Model
# ──────────────────────────────────────────────

class WorkflowStepModel(BaseModel):
    """A single workflow step linking order → task."""
    iri: str = Field("", description="Full IRI of the WorkflowStep individual")
    var_name: str = Field("", description="Canonical step variable name")
    step_order: int = Field(..., description="Integer step order")
    task_iri: str = Field("", description="Associated task IRI")
    task_var_name: str = Field(..., description="Associated task var_name")
    step_type: str = Field("WorkflowStep", description="StartStep / WorkflowStep / EndStep")
    next_step_iris: List[str] = Field(default_factory=list, description="Outgoing :nextStep targets")
    agent_iri: str = Field("", description="Resolved agent IRI from associated task")
    description: str = Field("", description="Step description")


class WorkflowPatternModel(BaseModel):
    """agentO :WorkflowPattern with topology and step membership."""
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
    """agentO :Memory represented without framework-specific storage classes."""
    iri: str
    var_name: str
    label: str = ""
    description: str = ""
    configs: Dict[str, str] = Field(default_factory=dict)


# ──────────────────────────────────────────────
# Input Variable Model
# ──────────────────────────────────────────────

class InputVariableModel(BaseModel):
    """A template placeholder variable extracted from prompts."""
    name: str = Field(..., description="Variable name (e.g. 'company_domain')")
    default_value: str = Field("", description="Default value if found in KG")
    has_default: bool = Field(False, description="True if KG provides a concrete default value")
    alternative_values: List[str] = Field(
        default_factory=list,
        description="Other example values from KG (non-default KickoffInputBundle entries)",
    )


class AgenticProject(BaseModel):
    """Framework-agnostic extraction result from a single KG file."""
    name: str
    var_name: str = ""
    description: str = ""
    team_iri: str = Field("", description="IRI of the :Team individual")
    agent_member_iris: List[str] = Field(default_factory=list, description=":hasAgentMember targets")
    workflow_pattern_iris: List[str] = Field(default_factory=list, description=":hasWorkflowPattern targets")
    goal_iris: List[str] = Field(default_factory=list, description="Team-level :hasGoal / :hasTeamGoal targets")
    objective_iris: List[str] = Field(default_factory=list, description="Team-level :hasObjective targets")

    # Core components
    agents: List[AgentModel] = Field(default_factory=list)
    tasks: List[TaskModel] = Field(default_factory=list)
    tools: List[ToolModel] = Field(default_factory=list)
    workflows: List[WorkflowPatternModel] = Field(default_factory=list)
    memories: List[MemoryModel] = Field(default_factory=list)
    language_models: List[LanguageModelModel] = Field(default_factory=list)
    input_variables: List[InputVariableModel] = Field(default_factory=list)
    env_vars: List[ConfigModel] = Field(default_factory=list)
    system_configs: Dict[str, str] = Field(default_factory=dict)

    # New ontology class collections
    goals: List[GoalModel] = Field(default_factory=list)
    capabilities: List[CapabilityModel] = Field(default_factory=list)
    environments: List[EnvironmentModel] = Field(default_factory=list)
    objectives: List[ObjectiveModel] = Field(default_factory=list)
    human_agents: List[HumanAgentModel] = Field(default_factory=list)
    resources: List[ResourceModel] = Field(default_factory=list)
    constraints: List[ConstraintModel] = Field(default_factory=list)
