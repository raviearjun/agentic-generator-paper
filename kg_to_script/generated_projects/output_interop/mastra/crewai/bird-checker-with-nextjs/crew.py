"""
Auto-generated CrewAI Crew: BirdCheckerSystem

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Identify if an image depicts a bird, provide the scientific name if it is a bird, and summarize the image location in one or two short sentences.
Capabilities:
  - : Fetch random image matching a query from the Unsplash API
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
            tools=[get_random_image_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def get_image_task(self) -> Task:
        return Task(
            config=self.tasks_config['get_image_task'],
        )

    @task
    def bird_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['bird_check_task'],
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
