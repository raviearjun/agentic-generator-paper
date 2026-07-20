"""
Auto-generated CrewAI Crew: UnnamedProject

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class UnnamedProject:
    """UnnamedProject crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
        )

    @agent
    def critic(self) -> Agent:
        return Agent(
            config=self.agents_config['critic'],
        )

    @agent
    def seo_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_reviewer'],
        )

    @agent
    def legal_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['legal_reviewer'],
        )

    @agent
    def ethics_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['ethics_reviewer'],
        )

    @agent
    def meta_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['meta_reviewer'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_write_blog(self) -> Task:
        return Task(
            config=self.tasks_config['task_write_blog'],
            agent=self.writer(),
        )

    @task
    def task_critic_initiate_1(self) -> Task:
        return Task(
            config=self.tasks_config['task_critic_initiate_1'],
            agent=self.critic(),
        )

    @task
    def task_nested_seo_review(self) -> Task:
        return Task(
            config=self.tasks_config['task_nested_seo_review'],
            agent=self.seo_reviewer(),
        )

    @task
    def task_nested_legal_review(self) -> Task:
        return Task(
            config=self.tasks_config['task_nested_legal_review'],
            agent=self.legal_reviewer(),
        )

    @task
    def task_nested_ethics_review(self) -> Task:
        return Task(
            config=self.tasks_config['task_nested_ethics_review'],
            agent=self.ethics_reviewer(),
        )

    @task
    def task_meta_aggregate(self) -> Task:
        return Task(
            config=self.tasks_config['task_meta_aggregate'],
            agent=self.meta_reviewer(),
        )

    @task
    def task_critic_initiate_2(self) -> Task:
        return Task(
            config=self.tasks_config['task_critic_initiate_2'],
            agent=self.critic(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the UnnamedProject"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
