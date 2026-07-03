"""
Auto-generated CrewAI Crew: SurpriseTravelCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Create a comprehensive surprise travel plan for the traveler covering activities, restaurants, and a day-by-day itinerary.
Capabilities:
  - : Performs web searches for information such as events, activities, and restaurant listings.
  - : Extracts structured information from web pages (addresses, ratings, descriptions).
  - : Research and recommend activities suitable to traveler preferences.
  - : Find and recommend restaurants and scenic dining locations.
  - : Compile research into a day-by-day itinerary document.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_serper_dev_tool — unknown tool class "ToolSerperDevTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSerperDevTool")
def tool_serper_dev_tool(*args, **kwargs) -> str:
    """Web search tool (Serper.dev) used to search the web for activities, restaurants, and general informa"""
    return "tool_serper_dev_tool result"

# TODO: tool_scrape_website_tool — unknown tool class "ToolScrapeWebsiteTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolScrapeWebsiteTool")
def tool_scrape_website_tool(*args, **kwargs) -> str:
    """Tool used to scrape website content for details about venues, restaurants and events."""
    return "tool_scrape_website_tool result"




@CrewBase
class SurpriseTravelCrew:
    """SurpriseTravelCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def personalized_activity_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['personalized_activity_planner'],
            tools=[tool_serper_dev_tool, tool_scrape_website_tool],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def restaurant_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['restaurant_scout'],
            tools=[tool_serper_dev_tool, tool_scrape_website_tool],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def itinerary_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_compiler'],
            tools=[tool_serper_dev_tool],
            allow_delegation=False,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_personalized_activity_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_personalized_activity_planning_task'],
            agent=self.personalized_activity_planner(),
        )

    @task
    def task_restaurant_scenic_location_scout_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_restaurant_scenic_location_scout_task'],
            agent=self.restaurant_scout(),
        )

    @task
    def task_itinerary_compilation_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_itinerary_compilation_task'],
            agent=self.itinerary_compiler(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the SurpriseTravelCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
