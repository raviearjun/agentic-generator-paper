"""
Auto-generated CrewAI Crew: CustomCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Define agent 1 goal here
  - : Define agent 2 goal here
Capabilities:
  - : Performs web searches and returns results
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_duck_duck_go_search_run — unknown tool class "ToolDuckDuckGoSearchRun"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolDuckDuckGoSearchRun")
def tool_duck_duck_go_search_run(*args, **kwargs) -> str:
    """LangChain DuckDuckGo search tool used for web search"""
    return "tool_duck_duck_go_search_run result"




@CrewBase
class CustomCrew:
    """CustomCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def agent_1_name(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_1_name'],
            tools=[tool_duck_duck_go_search_run],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def agent_2_name(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_2_name'],
            tools=[tool_duck_duck_go_search_run],
            allow_delegation=False,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_1(self) -> Task:
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_1_name(),
        )

    @task
    def task_2(self) -> Task:
        return Task(
            config=self.tasks_config['task_2'],
            agent=self.agent_2_name(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the CustomCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
