"""
Auto-generated CrewAI Crew: TripPlannerCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Select the best city based on weather, season, and prices
  - : Provide the BEST insights about the selected city
  - : Create the most amazing travel itineraries with budget and packing suggestions for the city
  - : Automate the process of choosing among city options and producing a full trip itinerary based on traveler preferences.
Capabilities:
  - : Search the internet for relevant results using Serper API.
  - : Scrape and summarize website content using browserless and HTML partitioning.
  - : Perform safe mathematical calculations.
  - : Analyze travel data to select an optimal city based on weather, season, and prices.
  - : Provide deep local insights, attractions, cultural context, and practical tips.
  - : Create detailed itineraries, budgets, packing suggestions, and logistics.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_search — unknown tool class "toolsearch"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearch")
def tool_search(*args, **kwargs) -> str:
    """Search the internet using Serper (google.serper.dev) and return top results."""
    return "tool_search result"

# TODO: tool_browser — unknown tool class "toolbrowser"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolbrowser")
def tool_browser(*args, **kwargs) -> str:
    """Scrape website content via browserless and summarize chunks using an internal Agent/Task."""
    return "tool_browser result"

# TODO: tool_calculator — unknown tool class "toolcalculator"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolcalculator")
def tool_calculator(*args, **kwargs) -> str:
    """Safe mathematical expression evaluator implemented with ast and restricted operators."""
    return "tool_calculator result"




@CrewBase
class TripPlannerCrew:
    """TripPlannerCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def city_selection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selection_agent'],
            tools=[tool_search, tool_browser],
            verbose=True,
        )

    @agent
    def local_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert_agent'],
            tools=[tool_search, tool_browser],
            verbose=True,
        )

    @agent
    def travel_concierge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge_agent'],
            tools=[tool_search, tool_browser, tool_calculator],
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_identify_city(self) -> Task:
        return Task(
            config=self.tasks_config['task_identify_city'],
            agent=self.city_selection_agent(),
        )

    @task
    def task_gather_city_info(self) -> Task:
        return Task(
            config=self.tasks_config['task_gather_city_info'],
            agent=self.local_expert_agent(),
        )

    @task
    def task_plan_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config['task_plan_itinerary'],
            agent=self.travel_concierge_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the TripPlannerCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
