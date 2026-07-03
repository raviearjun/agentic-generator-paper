"""
Auto-generated CrewAI Crew: mastrainstanceworkflowairecruiter

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class mastrainstanceworkflowairecruiter:
    """mastrainstanceworkflowairecruiter crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def mastra_llm(self) -> Agent:
        return Agent(
            config=self.agents_config['mastra_llm'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def gather_candidate_info_task(self) -> Task:
        return Task(
            config=self.tasks_config['gather_candidate_info_task'],
            agent=self.mastra_llm(),
        )

    @task
    def ask_about_specialty_task(self) -> Task:
        return Task(
            config=self.tasks_config['ask_about_specialty_task'],
            agent=self.mastra_llm(),
        )

    @task
    def ask_about_role_task(self) -> Task:
        return Task(
            config=self.tasks_config['ask_about_role_task'],
            agent=self.mastra_llm(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the mastrainstanceworkflowairecruiter"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
