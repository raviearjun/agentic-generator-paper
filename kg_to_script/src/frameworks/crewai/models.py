"""Framework-specific IR models for the CrewAI generator.

ProcessType is defined here (not in core) because it is a CrewAI concept:
  crewai.Process.sequential / crewai.Process.hierarchical
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from ...core.models import (
    AgentModel,
    CapabilityModel,
    ConfigModel,
    ConstraintModel,
    EnvironmentModel,
    GoalModel,
    HumanAgentModel,
    LanguageModelModel,
    ObjectiveModel,
    ResourceModel,
    TaskModel,
    ToolModel,
    WorkflowStepModel,
)


class ProcessType(str, Enum):
    """CrewAI process type — maps to crewai.Process enum values."""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"


class CrewProject(BaseModel):
    """Framework-specific IR for CrewAI generation."""

    crew_name: str = Field(..., description="CamelCase crew class name (e.g. 'GameBuilderCrew')")
    crew_var_name: str = Field("", description="snake_case module name (e.g. 'game_builder_crew')")
    description: str = Field("", description="Team-level description")
    process: ProcessType = Field(ProcessType.SEQUENTIAL, description="CrewAI workflow process type")

    agents: List[AgentModel] = Field(default_factory=list)
    tasks: List[TaskModel] = Field(default_factory=list)
    tools: List[ToolModel] = Field(default_factory=list)
    workflow_steps: List[WorkflowStepModel] = Field(default_factory=list)

    # Adapter-computed per-agent derived data (keyed by agent var_name)
    agent_allow_delegation: Dict[str, Optional[bool]] = Field(
        default_factory=dict,
        description="Computed allow_delegation per agent, read from agent.configs",
    )
    agent_verbose: Dict[str, Optional[bool]] = Field(
        default_factory=dict,
        description="Computed verbose per agent, read from agent.configs",
    )
    agent_tool_var_names: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Computed tool variable name list per agent, derived from tool_iris",
    )

    # Adapter-computed per-tool derived data (keyed by tool var_name)
    tool_class_names: Dict[str, str] = Field(
        default_factory=dict,
        description="CamelCase class name per tool (label → CamelCase, used by generator)",
    )

    language_models: List[LanguageModelModel] = Field(default_factory=list)
    env_vars: List[ConfigModel] = Field(
        default_factory=list,
        description="Environment variables needed (API keys etc.)",
    )

    human_agents: List[HumanAgentModel] = Field(default_factory=list)
    goals: List[GoalModel] = Field(default_factory=list)
    objectives: List[ObjectiveModel] = Field(default_factory=list)
    capabilities: List[CapabilityModel] = Field(default_factory=list)
    environments: List[EnvironmentModel] = Field(default_factory=list)
    resources: List[ResourceModel] = Field(default_factory=list)
    constraints: List[ConstraintModel] = Field(default_factory=list)
