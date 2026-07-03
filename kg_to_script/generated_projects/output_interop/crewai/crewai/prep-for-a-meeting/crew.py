"""
Auto-generated CrewAI Crew: MeetingPreparationCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Conduct thorough research on people and companies involved in the meeting.
  - : Analyze the current industry trends, challenges, and opportunities.
  - : Develop talking points, questions, and strategic angles for the meeting.
  - : Compile all gathered information into a concise, informative briefing document.
Capabilities:
  - : Performs web searches and returns search result identifiers.
  - : Finds webpages similar to a given URL.
  - : Retrieves and returns contents of webpages by IDs.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: exa_search_tool_search — unknown tool class "ExaSearchToolsearch"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ExaSearchToolsearch")
def exa_search_tool_search(*args, **kwargs) -> str:
    """Search for a webpage based on the query (returns a list of result IDs)."""
    return "exa_search_tool_search result"

# TODO: exa_search_tool_find_similar — unknown tool class "ExaSearchToolfindsimilar"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ExaSearchToolfindsimilar")
def exa_search_tool_find_similar(*args, **kwargs) -> str:
    """Search for webpages similar to a given URL."""
    return "exa_search_tool_find_similar result"

# TODO: exa_search_tool_get_contents — unknown tool class "ExaSearchToolgetcontents"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ExaSearchToolgetcontents")
def exa_search_tool_get_contents(*args, **kwargs) -> str:
    """Get the contents of webpages given a list of IDs."""
    return "exa_search_tool_get_contents result"




@CrewBase
class MeetingPreparationCrew:
    """MeetingPreparationCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_agent'],
            tools=[exa_search_tool_search, exa_search_tool_find_similar, exa_search_tool_get_contents],
            verbose=True,
        )

    @agent
    def industry_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['industry_analyst_agent'],
            tools=[exa_search_tool_search, exa_search_tool_find_similar, exa_search_tool_get_contents],
            verbose=True,
        )

    @agent
    def meeting_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['meeting_strategy_agent'],
            tools=[exa_search_tool_search, exa_search_tool_find_similar, exa_search_tool_get_contents],
            verbose=True,
        )

    @agent
    def summary_and_briefing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_and_briefing_agent'],
            tools=[exa_search_tool_search, exa_search_tool_find_similar, exa_search_tool_get_contents],
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher_agent(),
        )

    @task
    def industry_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['industry_analysis_task'],
            agent=self.industry_analyst_agent(),
        )

    @task
    def meeting_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['meeting_strategy_task'],
            agent=self.meeting_strategy_agent(),
        )

    @task
    def summary_and_briefing_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_and_briefing_task'],
            agent=self.summary_and_briefing_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MeetingPreparationCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
