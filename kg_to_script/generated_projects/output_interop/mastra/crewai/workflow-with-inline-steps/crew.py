"""
Auto-generated CrewAI Crew: mastraruntime

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class mastraruntime:
    """mastraruntime crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def mastra_default_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['mastra_default_agent'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_step_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_one'],
            agent=self.mastra_default_agent(),
        )

    @task
    def task_step_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_two'],
            agent=self.mastra_default_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the mastraruntime"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
