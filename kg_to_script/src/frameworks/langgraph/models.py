from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ...core.models import (
    CapabilityModel,
    ConstraintModel,
    EnvironmentModel,
    GoalModel,
    HumanAgentModel,
    ObjectiveModel,
    ResourceModel,
    TaskModel,
)


class LangGraphToolModel(BaseModel):
    """Represents a KG :Tool mapped to a LangGraph @tool stub."""

    iri: str = Field(..., description="Full IRI of the Tool individual")
    var_name: str = Field(..., description="Python variable name (snake_case)")
    title: str = Field("", description="Human-readable tool title")
    description: str = Field("A tool", description="Tool description for the @tool docstring")


class LangGraphAgentModel(BaseModel):
    """Represents a KG :LLMAgent mapped to a LangGraph node function."""

    iri: str = Field(..., description="Full IRI of the LLMAgent individual")
    var_name: str = Field(..., description="Python variable/function name (snake_case)")
    role: str = Field("agent", description="Agent role (used as node description)")
    prompt: str = Field("You are a helpful assistant.", description="System prompt injected as SystemMessage")
    model_name: str = Field("gpt-4o-mini", description="LLM model identifier")
    provider: str = Field("openai", description="LLM provider: 'openai' or 'anthropic'")
    tools_refs: List[str] = Field(default_factory=list, description="Tool IRI references assigned to this agent")


class LangGraphNodeModel(BaseModel):
    """Represents a workflow step mapped to a LangGraph node."""

    iri: str = Field(..., description="Full IRI of the WorkflowStep individual")
    name: str = Field(..., description="Node name (snake_case, used in add_node)")
    ts_name: str = Field(..., description="TypeScript-safe node name (lowerCamelCase)")
    agent_ref: Optional[str] = Field(None, description="IRI of the agent assigned to this node")
    node_kind: str = Field("worker", description="Node kind: router | worker | general_input | end")
    group: str = Field("core", description="Optional grouping label for file organization")
    is_start: bool = Field(False, description="True if this is the START node")
    is_end: bool = Field(False, description="True if this is the END node")


class LangGraphEdgeModel(BaseModel):
    """Represents a directed edge between two graph nodes."""

    source: str = Field(..., description="Source node IRI or name")
    target: str = Field(..., description="Target node IRI or name")
    condition: Optional[str] = Field(None, description="Optional condition label for routing")


class LangGraphRouteModel(BaseModel):
    """Represents a supervisor router destination."""

    source_node: str = Field(..., description="Router node ts_name")
    target_node: str = Field(..., description="Destination node ts_name")
    route_key: str = Field(..., description="Route key exposed in state.next")
    is_fallback: bool = Field(False, description="True when route is default fallback")


class LangGraphProject(BaseModel):
    """Framework-specific IR for LangGraph generation."""

    name: str = Field("LangGraph Project", description="Human-readable project name")
    tools: List[LangGraphToolModel] = Field(default_factory=list)
    agents: List[LangGraphAgentModel] = Field(default_factory=list)
    nodes: List[LangGraphNodeModel] = Field(default_factory=list)
    edges: List[LangGraphEdgeModel] = Field(default_factory=list)
    routes: List[LangGraphRouteModel] = Field(default_factory=list)
    router_node_name: str = Field("", description="Router node ts_name for supervisor graphs")
    start_node_name: str = Field("", description="Start node ts_name")
    workflow_names: List[str] = Field(
        default_factory=list,
        description="Original workflow identifiers from the KG (used in generated code comments for OEC matching)",
    )
    tasks: List[TaskModel] = Field(default_factory=list, description="Original tasks for human_input detection in templates")

    human_agents: List[HumanAgentModel] = Field(default_factory=list)
    goals: List[GoalModel] = Field(default_factory=list)
    objectives: List[ObjectiveModel] = Field(default_factory=list)
    capabilities: List[CapabilityModel] = Field(default_factory=list)
    environments: List[EnvironmentModel] = Field(default_factory=list)
    resources: List[ResourceModel] = Field(default_factory=list)
    constraints: List[ConstraintModel] = Field(default_factory=list)

    @property
    def pattern_type(self) -> str:
        # Supervisor requires an explicit named router node AND computed routes.
        # Graphs that simply have branching edges (out-degree > 1 on a non-router node)
        # are NOT supervisors — they are general branching DAGs.
        if self.router_node_name and self.routes:
            return "supervisor"
        # If there are explicit topology edges defined, emit the full DAG faithfully.
        if self.edges:
            return "branching"
        if self.tools:
            return "tool_calling"
        return "linear"
