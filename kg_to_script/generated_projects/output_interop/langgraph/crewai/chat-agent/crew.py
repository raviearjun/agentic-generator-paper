"""
Auto-generated CrewAI Crew: StateGraphTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class StateGraphTeam:
    """StateGraphTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def chat_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chat_agent'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_chat(self) -> Task:
        return Task(
            config=self.tasks_config['task_chat'],
            agent=self.chat_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the StateGraphTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
