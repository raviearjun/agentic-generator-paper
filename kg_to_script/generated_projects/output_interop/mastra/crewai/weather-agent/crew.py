"""
Auto-generated CrewAI Crew: mastrainstance

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Provide concise weather information including humidity, wind, precipitation; ask for location if not provided.
  - : Fetch current weather and geocoding for a given location using Open-Meteo APIs.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_get_weather — unknown tool class "toolgetweather"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolgetweather")
def tool_get_weather(*args, **kwargs) -> str:
    """Get current weather for a location"""
    return "tool_get_weather result"




@CrewBase
class mastrainstance:
    """mastrainstance crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def weather_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_agent'],
            tools=[tool_get_weather],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_fetch_weather(self) -> Task:
        return Task(
            config=self.tasks_config['task_fetch_weather'],
            agent=self.weather_agent(),
        )

    @task
    def task_plan_activities(self) -> Task:
        return Task(
            config=self.tasks_config['task_plan_activities'],
            agent=self.weather_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the mastrainstance"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
