"""
Auto-generated CrewAI Crew: GroupChatTeamforBlogGeneration

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class GroupChatTeamforBlogGeneration:
    """GroupChatTeamforBlogGeneration crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def admin(self) -> Agent:
        return Agent(
            config=self.agents_config['admin'],
        )

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'],
        )

    @agent
    def engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['engineer'],
        )

    @agent
    def executor(self) -> Agent:
        return Agent(
            config=self.agents_config['executor'],
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
        )

    @agent
    def group_chat_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['group_chat_manager'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_initiate_write_blog(self) -> Task:
        return Task(
            config=self.tasks_config['task_initiate_write_blog'],
            agent=self.admin(),
        )

    @task
    def task_planner_plan(self) -> Task:
        return Task(
            config=self.tasks_config['task_planner_plan'],
            agent=self.planner(),
        )

    @task
    def task_engineer_write_code(self) -> Task:
        return Task(
            config=self.tasks_config['task_engineer_write_code'],
            agent=self.engineer(),
        )

    @task
    def task_executor_run_code(self) -> Task:
        return Task(
            config=self.tasks_config['task_executor_run_code'],
            agent=self.executor(),
        )

    @task
    def task_writer_produce_blog(self) -> Task:
        return Task(
            config=self.tasks_config['task_writer_produce_blog'],
            agent=self.writer(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the GroupChatTeamforBlogGeneration"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
