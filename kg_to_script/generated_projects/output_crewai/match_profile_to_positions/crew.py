"""
Auto-generated CrewAI Crew: MatchToProposalCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Extract relevant information from the CV, such as skills, experience, and education.
  - : Match the CV to the job opportunities based on skills, experience, and key achievements.
  - : Overall objective for the crew: automate the matching of candidate CVs to job proposals.
Capabilities:
  - : Capability to read file contents from disk.
  - : Capability to search and query CSV-formatted job listings.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_file_read — unknown tool class "toolfileread"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolfileread")
def tool_file_read(*args, **kwargs) -> str:
    """Tool to read file contents (used to read CV and other files)."""
    return "tool_file_read result"

# TODO: tool_csv_search — unknown tool class "toolcsvsearch"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolcsvsearch")
def tool_csv_search(*args, **kwargs) -> str:
    """Tool to search and query CSV files for matching job opportunities."""
    return "tool_csv_search result"




@CrewBase
class MatchToProposalCrew:
    """MatchToProposalCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reader'],
            tools=[tool_file_read],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[tool_file_read, tool_csv_search],
            allow_delegation=False,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_read_cv(self) -> Task:
        return Task(
            config=self.tasks_config['task_read_cv'],
            agent=self.cv_reader(),
        )

    @task
    def task_match_cv(self) -> Task:
        return Task(
            config=self.tasks_config['task_match_cv'],
            agent=self.matcher(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MatchToProposalCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
