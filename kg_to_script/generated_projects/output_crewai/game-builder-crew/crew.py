"""
Auto-generated CrewAI Crew: GameBuilderCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Create software as needed
  - : Create Perfect code, by analyzing the code that is given for errors
  - : Ensure that the code does the job that it is supposed to do
  - : Automate the creation of a Python-based game using autonomous agents orchestrated by the CrewAI framework.
Capabilities:
  - : Web search and retrieval capability (e.g., Serper).
  - : Access to OpenAI language model API.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_serper — unknown tool class "toolserper"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolserper")
def tool_serper(*args, **kwargs) -> str:
    """Serper search API used for web search (mentioned in README)."""
    return "tool_serper result"

# TODO: tool_openai_api — unknown tool class "toolopenaiapi"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolopenaiapi")
def tool_openai_api(*args, **kwargs) -> str:
    """OpenAI API access used by CrewAI to call LLMs (configured via environment variables)."""
    return "tool_openai_api result"




@CrewBase
class GameBuilderCrew:
    """GameBuilderCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def senior_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_agent'],
            tools=[tool_serper, tool_openai_api],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer_agent'],
            tools=[tool_serper, tool_openai_api],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def chief_qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_qa_engineer_agent'],
            tools=[tool_serper, tool_openai_api],
            allow_delegation=True,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_code(self) -> Task:
        return Task(
            config=self.tasks_config['task_code'],
            agent=self.senior_engineer_agent(),
        )

    @task
    def task_review(self) -> Task:
        return Task(
            config=self.tasks_config['task_review'],
            agent=self.qa_engineer_agent(),
        )

    @task
    def task_evaluate(self) -> Task:
        return Task(
            config=self.tasks_config['task_evaluate'],
            agent=self.chief_qa_engineer_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the GameBuilderCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
