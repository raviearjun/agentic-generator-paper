"""
Auto-generated CrewAI Crew: MastraInstance

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : 
  - : 
  - : 
  - : 
  - : 
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_search_flights — unknown tool class "toolsearchFlights"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearchFlights")
def tool_search_flights(*args, **kwargs) -> str:
    """Fetches flight information for a given date range, origin and destination. Origin and Destination ar"""
    return "tool_search_flights result"

# TODO: tool_search_hotels — unknown tool class "toolsearchHotels"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearchHotels")
def tool_search_hotels(*args, **kwargs) -> str:
    """Searches for hotels in a specified location. Destination is a cityId like 20015732 for 20015733"""
    return "tool_search_hotels result"

# TODO: tool_search_attractions — unknown tool class "toolsearchAttractions"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearchAttractions")
def tool_search_attractions(*args, **kwargs) -> str:
    """Searches for attractions in a specified location. Destination is a cityId like 20015732 for 20015733"""
    return "tool_search_attractions result"

# TODO: tool_search_airbnb_location — unknown tool class "toolsearchAirbnbLocation"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearchAirbnbLocation")
def tool_search_airbnb_location(*args, **kwargs) -> str:
    """Searches for Airbnb places in a specified location. Place is a city name like New York, NY"""
    return "tool_search_airbnb_location result"

# TODO: tool_search_airbnb — unknown tool class "toolsearchAirbnb"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearchAirbnb")
def tool_search_airbnb(*args, **kwargs) -> str:
    """Searches for Airbnb in a specified location. Place is a cityId like 20015732 for 20015733"""
    return "tool_search_airbnb result"




@CrewBase
class MastraInstance:
    """MastraInstance crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def travel_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_agent'],
            tools=[tool_search_flights, tool_search_hotels, tool_search_attractions, tool_search_airbnb_location, tool_search_airbnb],
        )

    @agent
    def travel_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_analyzer'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_outbound_flight(self) -> Task:
        return Task(
            config=self.tasks_config['task_outbound_flight'],
            agent=self.travel_analyzer(),
        )

    @task
    def task_sync_csv_data(self) -> Task:
        return Task(
            config=self.tasks_config['task_sync_csv_data'],
            agent=self.travel_analyzer(),
        )

    @task
    def task_return_flight(self) -> Task:
        return Task(
            config=self.tasks_config['task_return_flight'],
            agent=self.travel_analyzer(),
        )

    @task
    def task_accommodation_hotels(self) -> Task:
        return Task(
            config=self.tasks_config['task_accommodation_hotels'],
            agent=self.travel_analyzer(),
        )

    @task
    def task_attraction(self) -> Task:
        return Task(
            config=self.tasks_config['task_attraction'],
            agent=self.travel_analyzer(),
        )

    @task
    def task_airbnb_location(self) -> Task:
        return Task(
            config=self.tasks_config['task_airbnb_location'],
            agent=self.travel_analyzer(),
        )

    @task
    def task_accommodation_airbnb(self) -> Task:
        return Task(
            config=self.tasks_config['task_accommodation_airbnb'],
            agent=self.travel_analyzer(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MastraInstance"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
