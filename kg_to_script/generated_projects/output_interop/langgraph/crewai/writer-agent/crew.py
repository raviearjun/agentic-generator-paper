"""
Auto-generated CrewAI Crew: WriterStateGraphTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Creates an initial draft document (short title and short description) given title/description inputs.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_draft_text_document — unknown tool class "tooldrafttextdocument"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("tooldrafttextdocument")
def tool_draft_text_document(*args, **kwargs) -> str:
    """Prepare a text document for the user with a short title and short description for browsing purposes."""
    return "tool_draft_text_document result"




@CrewBase
class WriterStateGraphTeam:
    """WriterStateGraphTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            tools=[tool_draft_text_document],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_prepare(self) -> Task:
        return Task(
            config=self.tasks_config['task_prepare'],
            agent=self.writer_agent(),
        )

    @task
    def task_writer(self) -> Task:
        return Task(
            config=self.tasks_config['task_writer'],
            agent=self.writer_agent(),
        )

    @task
    def task_suggestions(self) -> Task:
        return Task(
            config=self.tasks_config['task_suggestions'],
            agent=self.writer_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the WriterStateGraphTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
