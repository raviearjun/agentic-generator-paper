"""
Auto-generated CrewAI Crew: TripPlannerAppTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Creates and confirms accommodation bookings (receives accommodation and trip details, returns booking confirmation and details).
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: book_accommodation_tool — unknown tool class "BookAccommodationTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("BookAccommodationTool")
def book_accommodation_tool(*args, **kwargs) -> str:
    """Tool invoked to create an accommodation booking using provided order details (accommodation, tripDet"""
    return "book_accommodation_tool result"




@CrewBase
class TripPlannerAppTeam:
    """TripPlannerAppTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def trip_planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trip_planner_agent'],
            tools=[book_accommodation_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def view_accommodations_task(self) -> Task:
        return Task(
            config=self.tasks_config['view_accommodations_task'],
            agent=self.trip_planner_agent(),
        )

    @task
    def select_accommodation_task(self) -> Task:
        return Task(
            config=self.tasks_config['select_accommodation_task'],
            agent=self.trip_planner_agent(),
        )

    @task
    def confirm_booking_task(self) -> Task:
        return Task(
            config=self.tasks_config['confirm_booking_task'],
            agent=self.trip_planner_agent(),
        )

    @task
    def booked_confirmation_task(self) -> Task:
        return Task(
            config=self.tasks_config['booked_confirmation_task'],
            agent=self.trip_planner_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the TripPlannerAppTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
