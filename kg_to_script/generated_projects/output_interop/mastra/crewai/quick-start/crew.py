"""
Auto-generated CrewAI Crew: mastrainstance

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : No explicit goal provided in source; placeholder goal.
  - : No explicit goal provided in source; placeholder goal.
Capabilities:
  - : Execute workflow step code and perform system actions (e.g., logging).
Resources:
  - : Schema-constrained output object with property 'species'.
  - : Output of logCatName step (rawText value).
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: mastra_runtime — unknown tool class "mastraRuntime"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("mastraRuntime")
def mastra_runtime(*args, **kwargs) -> str:
    """Runtime engine that executes workflow step code (non-LLM execution)."""
    return "mastra_runtime result"




@CrewBase
class mastrainstance:
    """mastrainstance crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def cat_one(self) -> Agent:
        return Agent(
            config=self.agents_config['cat_one'],
        )

    @agent
    def agent_two(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_two'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_log_cat_name(self) -> Task:
        return Task(
            config=self.tasks_config['task_log_cat_name'],
        )

    @task
    def task_generate_species(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_species'],
            agent=self.cat_one(),
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
