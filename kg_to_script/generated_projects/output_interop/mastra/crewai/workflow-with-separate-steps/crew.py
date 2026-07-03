"""
Auto-generated CrewAI Crew: mastrainstance

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : 
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class mastrainstance:
    """mastrainstance crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def mastra_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['mastra_agent'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_step_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_one'],
            agent=self.mastra_agent(),
        )

    @task
    def task_step_three(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_three'],
            agent=self.mastra_agent(),
        )

    @task
    def task_step_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_two'],
            agent=self.mastra_agent(),
        )

    @task
    def task_step_four(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_four'],
            agent=self.mastra_agent(),
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
