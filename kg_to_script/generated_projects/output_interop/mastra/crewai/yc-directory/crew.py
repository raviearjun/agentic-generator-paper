"""
Auto-generated CrewAI Crew: MastraInstanceycagent

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Returns an array of company records with fields: name, longDescription, tags, industries, batch.
  - : Ability to answer questions using the 2024 YC directory dataset.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: yc_directory_tool — unknown tool class "YCDirectoryTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("YCDirectoryTool")
def yc_directory_tool(*args, **kwargs) -> str:
    """Get data from the 2024 YC directory"""
    return "yc_directory_tool result"




@CrewBase
class MastraInstanceycagent:
    """MastraInstanceycagent crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def yc_directory_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['yc_directory_agent'],
            tools=[yc_directory_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def fetch_yc_directory_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_yc_directory_task'],
            agent=self.yc_directory_agent(),
        )

    @task
    def process_yc_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['process_yc_data_task'],
            agent=self.yc_directory_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MastraInstanceycagent"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
