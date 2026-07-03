"""
Auto-generated CrewAI Crew: BirdCheckerSystem

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Determine whether an image contains a bird, identify the species, and summarize the location.
Capabilities:
  - : Classify images as bird/non-bird, identify species, and summarize location.
  - : Search Unsplash and return a random image matching a query (returns imageUrl, photographerName, photographerProfile).
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: get_random_image_tool — unknown tool class "getRandomImageTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("getRandomImageTool")
def get_random_image_tool(*args, **kwargs) -> str:
    """Gets a random image from Unsplash based on the selected option"""
    return "get_random_image_tool result"




@CrewBase
class BirdCheckerSystem:
    """BirdCheckerSystem crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def bird_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['bird_checker'],
            tools=[get_random_image_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def get_random_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['get_random_image_task'],
        )

    @task
    def image_metadata_task(self) -> Task:
        return Task(
            config=self.tasks_config['image_metadata_task'],
            agent=self.bird_checker(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the BirdCheckerSystem"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
