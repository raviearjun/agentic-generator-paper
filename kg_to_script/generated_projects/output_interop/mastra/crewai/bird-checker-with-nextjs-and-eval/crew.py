"""
Auto-generated CrewAI Crew: BirdCheckerSystem

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : System should determine whether a provided image contains a bird, identify its scientific name if present, and summarize location.
Capabilities:
  - : Fetch a random image from Unsplash matching the given query (wildlife | feathers | flying | birds).
Resources:
  - : Image object returned from Unsplash (urls, alt_description, user metadata).
  - : Structured classification output { bird: boolean, species: string, location: string }.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: get_random_image_tool — unknown tool class "GetRandomImageTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("GetRandomImageTool")
def get_random_image_tool(*args, **kwargs) -> str:
    """Gets a random image from unsplash based on the selected option"""
    return "get_random_image_tool result"




@CrewBase
class BirdCheckerSystem:
    """BirdCheckerSystem crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def bird_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['bird_agent'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def get_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['get_image_task'],
        )

    @task
    def classify_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['classify_image_task'],
            agent=self.bird_agent(),
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
