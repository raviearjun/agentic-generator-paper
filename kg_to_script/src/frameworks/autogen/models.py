from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from ...core.models import (
    AgentModel,
    CapabilityModel,
    ConfigModel,
    ConstraintModel,
    EnvironmentModel,
    GoalModel,
    HumanAgentModel,
    ObjectiveModel,
    ResourceModel,
    TaskModel,
    ToolModel,
    WorkflowPatternModel,
    WorkflowType,
)


class AutoGenProject(BaseModel):
    """Adapter output for the AutoGen generator."""

    name: str
    model_name: str = "gpt-4o-mini"
    team_type: str = "RoundRobinGroupChat"
    agents: List[AgentModel] = Field(default_factory=list)
    tasks: List[TaskModel] = Field(default_factory=list)
    workflows: List[WorkflowPatternModel] = Field(default_factory=list)
    tools: List[ToolModel] = Field(default_factory=list)
    ordered_tasks: List[TaskModel] = Field(default_factory=list)
    env_vars: List[ConfigModel] = Field(default_factory=list)

    human_agents: List[HumanAgentModel] = Field(default_factory=list)
    goals: List[GoalModel] = Field(default_factory=list)
    objectives: List[ObjectiveModel] = Field(default_factory=list)
    capabilities: List[CapabilityModel] = Field(default_factory=list)
    environments: List[EnvironmentModel] = Field(default_factory=list)
    resources: List[ResourceModel] = Field(default_factory=list)
    constraints: List[ConstraintModel] = Field(default_factory=list)
