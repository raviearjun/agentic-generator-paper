"""
Layer 2 – Pydantic Intermediate Representation (IR)

Strongly-typed data models that sit between SPARQL extraction (Layer 1)
and file generation (Layer 3).  Every field maps to a concrete CrewAI
YAML/Python construct, making the pipeline deterministic and testable.

Mapping overview:
    KG :LLMAgent      → AgentModel      → agents.yaml entry + crew.py @agent
    KG :Task           → TaskModel       → tasks.yaml entry  + crew.py @task
    KG :Tool           → ToolModel       → crew.py tool import / instantiation
    KG :Team           → CrewModel       → crew.py @crew + main.py
    KG :WorkflowStep   → WorkflowStepModel → task ordering in crew.py
    KG :Config         → ConfigModel     → .env / agent llm / etc.
    KG :LanguageModel  → LanguageModelModel → agent llm param
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


# ──────────────────────────────────────────────
# Leaf Models
# ──────────────────────────────────────────────

class ConfigModel(BaseModel):
    """A single key-value configuration entry from KG :Config."""
    key: str = Field(..., description="Config key (e.g. 'role', 'api_key', 'process')")
    value: str = Field(..., description="Config value")


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
    class_name: str = Field("", description="Inferred CrewAI tool class (e.g. 'SerperDevTool')")
    description: str = Field("", description="Tool description")
    configs: List[ToolConfigModel] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)


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
    goal: str = Field(..., description="Agent goal")
    backstory: str = Field(..., description="Agent backstory / system prompt")

    # crew.py fields
    tool_var_names: List[str] = Field(default_factory=list, description="Tool variable names")
    llm: Optional[LanguageModelModel] = Field(None, description="Language model if not default")
    allow_delegation: Optional[bool] = Field(None, description="Allow delegation flag")
    verbose: Optional[bool] = Field(None, description="Verbose flag (None = not specified in KG → omit from output)")


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

    # tasks.yaml fields
    description: str = Field(..., description="Task description (may contain {placeholders})")
    expected_output: str = Field(..., description="Expected output description")

    # crew.py fields
    agent_var_name: str = Field("", description="Assigned agent's var_name")
    context_task_var_names: List[str] = Field(
        default_factory=list,
        description="Prior task var_names this task depends on (requiresResource chain)"
    )
    output_json_model: Optional[str] = Field(
        None,
        description="Pydantic model name for structured JSON output"
    )


# ──────────────────────────────────────────────
# Workflow Step Model
# ──────────────────────────────────────────────

class WorkflowStepModel(BaseModel):
    """A single workflow step linking order → task."""
    step_order: int = Field(..., description="Integer step order")
    task_var_name: str = Field(..., description="Associated task var_name")
    step_type: str = Field("WorkflowStep", description="StartStep / WorkflowStep / EndStep")


# ──────────────────────────────────────────────
# Input Variable Model
# ──────────────────────────────────────────────

class InputVariableModel(BaseModel):
    """A template placeholder variable extracted from prompts."""
    name: str = Field(..., description="Variable name (e.g. 'company_domain')")
    default_value: str = Field("", description="Default value if found in KG")


# ──────────────────────────────────────────────
# Top-level Crew Model
# ──────────────────────────────────────────────

class CrewProject(BaseModel):
    """
    Complete intermediate representation for one CrewAI project.

    This is the single data structure passed from Layer 1 → Layer 3.
    It contains all information needed to generate:
      - config/agents.yaml
      - config/tasks.yaml
      - crew.py
      - main.py
      - .env (optional)
    """
    # Metadata
    crew_name: str = Field(..., description="CamelCase crew class name (e.g. 'GameBuilderCrew')")
    crew_var_name: str = Field("", description="snake_case module name (e.g. 'game_builder_crew')")
    description: str = Field("", description="Team-level description")
    process: ProcessType = Field(ProcessType.SEQUENTIAL, description="Workflow process type")

    # Components
    agents: List[AgentModel] = Field(default_factory=list)
    tasks: List[TaskModel] = Field(default_factory=list)
    tools: List[ToolModel] = Field(default_factory=list)
    workflow_steps: List[WorkflowStepModel] = Field(default_factory=list)

    # Runtime
    input_variables: List[InputVariableModel] = Field(
        default_factory=list,
        description="Template variables for crew.kickoff(inputs={...})"
    )
    language_models: List[LanguageModelModel] = Field(default_factory=list)

    # Environment
    env_vars: List[ConfigModel] = Field(
        default_factory=list,
        description="Environment variables needed (API keys etc.)"
    )
