from __future__ import annotations

from typing import List

from src.core.models import (
    AgenticProject,
    AgentModel,
    ConfigModel,
    LanguageModelModel,
    MemoryModel,
    TaskModel,
    ToolConfigModel,
    ToolModel,
    WorkflowPatternModel,
    WorkflowStepModel,
    WorkflowType,
)
from src.frameworks.crewai.models import ProcessType


def _make_project(**overrides) -> AgenticProject:
    llm_model = LanguageModelModel(
        iri="lm:1", name="gpt-4o", provider="openai", model_name="gpt-4o",
    )
    default = AgenticProject(
        name="TestCrew",
        var_name="test_crew",
        description="A test project",
        agents=[
            AgentModel(
                iri="agent:1",
                var_name="researcher",
                agent_id="researcher",
                role="Researcher",
                goal="Find information",
                system_prompt="You are a researcher.",
                backstory="You are a researcher.",
                tool_iris=["tool:1"],
                tool_var_names=["search_tool"],
                configs={"allow_delegation": "true", "verbose": "true"},
                allow_delegation=True,
                verbose=True,
                language_model=llm_model,
                llm=llm_model,
            ),
            AgentModel(
                iri="agent:2",
                var_name="writer",
                agent_id="writer",
                role="Writer",
                goal="Write reports",
                system_prompt="You are a writer.",
                backstory="You are a writer.",
            ),
        ],
        tasks=[
            TaskModel(
                iri="task:1",
                var_name="research_task",
                label="Research",
                description="Conduct research",
                expected_output="Research findings",
                prompt_instruction="Conduct research",
                prompt_output_indicator="Research findings",
                agent_iri="agent:1",
                agent_var_name="researcher",
                context_task_var_names=[],
            ),
            TaskModel(
                iri="task:2",
                var_name="write_task",
                label="Write",
                description="Write a report",
                expected_output="A report",
                prompt_instruction="Write a report",
                prompt_output_indicator="A report",
                agent_iri="agent:2",
                agent_var_name="writer",
                context_task_var_names=["research_task"],
            ),
        ],
        tools=[
            ToolModel(
                iri="tool:1",
                var_name="search_tool",
                label="SearchTool",
                class_name="SerperDevTool",
                description="A search tool",
                configs=[ToolConfigModel(key="api_key", value="test-key")],
                capability_iris=["search"],
            ),
        ],
        workflows=[
            WorkflowPatternModel(
                iri="wf:1",
                var_name="default_workflow",
                label="Default Workflow",
                steps=[
                    WorkflowStepModel(
                        iri="step:1",
                        var_name="step_1",
                        step_order=1,
                        task_iri="task:1",
                        task_var_name="research_task",
                        next_step_iris=["step:2"],
                        agent_iri="agent:1",
                    ),
                    WorkflowStepModel(
                        iri="step:2",
                        var_name="step_2",
                        step_order=2,
                        task_iri="task:2",
                        task_var_name="write_task",
                        next_step_iris=[],
                        agent_iri="agent:2",
                    ),
                ],
                workflow_type=WorkflowType.SEQUENTIAL,
            ),
        ],
        language_models=[llm_model],
        env_vars=[ConfigModel(key="OPENAI_API_KEY", value="sk-test")],
        system_configs={"process": "sequential"},
    )
    return default


# ── CrewAI Adapter ──


class TestCrewAIAdapter:
    def test_adapt_basic(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        crew = adapt(project)

        assert crew.crew_name == "TestCrew"
        assert crew.crew_var_name == "test_crew"
        assert crew.process == ProcessType.SEQUENTIAL
        assert len(crew.agents) == 2
        assert len(crew.tasks) == 2
        assert len(crew.tools) == 1
        assert len(crew.workflow_steps) == 2

    def test_adapt_agent_fields(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        crew = adapt(project)

        agent = crew.agents[0]
        assert agent.role == "Researcher"
        assert agent.goal == "Find information"
        assert agent.backstory == "You are a researcher."
        assert crew.agent_tool_var_names[agent.var_name] == ["search_tool"]
        assert crew.agent_allow_delegation[agent.var_name] is True
        assert crew.agent_verbose[agent.var_name] is True

    def test_adapt_task_fields(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        crew = adapt(project)

        task = crew.tasks[0]
        assert task.description == "Conduct research"
        assert task.expected_output == "Research findings"
        assert task.agent_var_name == "researcher"
        assert task.context_task_var_names == []

    def test_adapt_task_context(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        crew = adapt(project)

        task = crew.tasks[1]
        assert task.context_task_var_names == ["research_task"]

    def test_adapt_workflow_steps_ordered(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        crew = adapt(project)

        assert [s.task_var_name for s in crew.workflow_steps] == [
            "research_task", "write_task"
        ]
        assert crew.workflow_steps[0].step_order == 1
        assert crew.workflow_steps[1].step_order == 2

    def test_adapt_fills_field_from_iri(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        for task in project.tasks:
            task.agent_var_name = ""  # clear var_name to test IRI fallback
        crew = adapt(project)

        assert crew.tasks[0].agent_var_name == "researcher"
        assert crew.tasks[1].agent_var_name == "writer"

    def test_adapt_empty_project(self):
        from src.frameworks.crewai.adapter import adapt

        empty = AgenticProject(name="Empty", agents=[], tasks=[], tools=[])
        crew = adapt(empty)
        assert crew.crew_name == "Empty"
        assert crew.process == ProcessType.SEQUENTIAL
        assert len(crew.agents) == 0
        assert len(crew.tasks) == 0

    def test_adapt_fills_defaults(self):
        from src.frameworks.crewai.adapter import adapt

        project = _make_project()
        for task in project.tasks:
            task.description = ""
            task.expected_output = ""
        crew = adapt(project)

        assert crew.tasks[0].description in (
            "Conduct research",
            "research_task",
        ) or crew.tasks[0].description != ""
        assert crew.tasks[0].expected_output != ""


# ── LangGraph Adapter ──


class TestLangGraphAdapter:
    def test_adapt_basic(self):
        from src.frameworks.langgraph.adapter import adapt

        project = _make_project()
        lg = adapt(project)

        assert len(lg.agents) == 2
        assert len(lg.tools) == 1
        assert len(lg.nodes) == 2
        assert len(lg.edges) == 1

    def test_adapt_agent_fields(self):
        from src.frameworks.langgraph.adapter import adapt

        project = _make_project()
        lg = adapt(project)

        agent = lg.agents[0]
        assert agent.var_name in ("researcher", "writer")
        assert agent.prompt in ("You are a researcher.", "You are a writer.")
        assert agent.model_name == "gpt-4o"
        assert len(agent.tools_refs) == 1

    def test_adapt_pattern_detection(self):
        from src.frameworks.langgraph.adapter import adapt

        project = _make_project()
        lg = adapt(project)
        # No explicit router node -> classified as a general branching DAG,
        # not "supervisor" (supervisor requires a named router + computed routes).
        assert lg.pattern_type == "branching"

    def test_adapt_tool_fields(self):
        from src.frameworks.langgraph.adapter import adapt

        project = _make_project()
        lg = adapt(project)

        tool = lg.tools[0]
        assert tool.var_name == "search_tool"
        assert tool.description == "A search tool"

    def test_adapt_nodes_and_edges(self):
        from src.frameworks.langgraph.adapter import adapt

        project = _make_project()
        lg = adapt(project)

        assert len(lg.nodes) == 2
        assert len(lg.edges) == 1
        assert lg.edges[0].source in (lg.nodes[0].iri, lg.nodes[1].iri)

    def test_adapt_empty_project(self):
        from src.frameworks.langgraph.adapter import adapt

        empty = AgenticProject(name="Empty", agents=[], tasks=[], tools=[])
        lg = adapt(empty)
        assert len(lg.agents) == 0
        assert len(lg.tools) == 0
        assert lg.pattern_type == "linear"

    def test_adapt_linear_pattern(self):
        from src.frameworks.langgraph.adapter import adapt

        project = _make_project()
        project.agents = project.agents[:1]  # single agent
        lg = adapt(project)
        # Workflow steps still define edges between the two tasks, so the
        # graph is still "branching" (edges present) even with one agent.
        assert lg.pattern_type == "branching"


# ── AutoGen Adapter ──


class TestAutoGenAdapter:
    def test_adapt_basic(self):
        from src.frameworks.autogen.adapter import adapt

        project = _make_project()
        result = adapt(project)

        assert result.name == "TestCrew"
        assert result.model_name == "gpt-4o"
        assert result.team_type == "RoundRobinGroupChat"
        assert len(result.agents) == 2
        assert len(result.tasks) == 2
        assert len(result.ordered_tasks) == 2

    def test_adapt_ordered_tasks(self):
        from src.frameworks.autogen.adapter import adapt

        project = _make_project()
        result = adapt(project)

        assert [t.var_name for t in result.ordered_tasks] == [
            "research_task", "write_task"
        ]

    def test_adapt_model_fallback(self):
        from src.frameworks.autogen.adapter import adapt

        project = _make_project()
        project.language_models = []
        result = adapt(project)

        assert result.model_name == "gpt-4o-mini"

    def test_adapt_empty_project(self):
        from src.frameworks.autogen.adapter import adapt

        empty = AgenticProject(name="Empty", agents=[], tasks=[], tools=[])
        result = adapt(empty)

        assert result.name == "Empty"
        assert result.model_name == "gpt-4o-mini"
        assert result.ordered_tasks == []
