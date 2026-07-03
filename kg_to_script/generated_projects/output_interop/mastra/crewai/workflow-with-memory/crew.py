"""
Auto-generated CrewAI Crew: mastrainstance

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Returns a cat fact string from an external API (catfact.ninja).
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_get_cat_facts — unknown tool class "toolGetCatFacts"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolGetCatFacts")
def tool_get_cat_facts(*args, **kwargs) -> str:
    """Fetches cat facts"""
    return "tool_get_cat_facts result"




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
            tools=[tool_get_cat_facts],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_step_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_one'],
            agent=self.cat_one(),
        )

    @task
    def task_par_step_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_par_step_one'],
            agent=self.cat_one(),
        )

    @task
    def task_br_step_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_br_step_one'],
            agent=self.cat_one(),
        )

    @task
    def task_cyc_step_one(self) -> Task:
        return Task(
            config=self.tasks_config['task_cyc_step_one'],
            agent=self.cat_one(),
        )

    @task
    def task_step_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_two'],
            agent=self.cat_one(),
        )

    @task
    def task_par_step_six(self) -> Task:
        return Task(
            config=self.tasks_config['task_par_step_six'],
            agent=self.cat_one(),
        )

    @task
    def task_br_step_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_br_step_two'],
            agent=self.cat_one(),
        )

    @task
    def task_cyc_step_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_cyc_step_two'],
            agent=self.cat_one(),
        )

    @task
    def task_step_three(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_three'],
            agent=self.cat_one(),
        )

    @task
    def task_par_step_two(self) -> Task:
        return Task(
            config=self.tasks_config['task_par_step_two'],
            agent=self.cat_one(),
        )

    @task
    def task_br_step_four(self) -> Task:
        return Task(
            config=self.tasks_config['task_br_step_four'],
            agent=self.cat_one(),
        )

    @task
    def task_cyc_step_three(self) -> Task:
        return Task(
            config=self.tasks_config['task_cyc_step_three'],
            agent=self.cat_one(),
        )

    @task
    def task_step_four(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_four'],
            agent=self.cat_one(),
        )

    @task
    def task_par_step_three(self) -> Task:
        return Task(
            config=self.tasks_config['task_par_step_three'],
            agent=self.cat_one(),
        )

    @task
    def task_br_step_three(self) -> Task:
        return Task(
            config=self.tasks_config['task_br_step_three'],
            agent=self.cat_one(),
        )

    @task
    def task_cyc_step_one_loop(self) -> Task:
        return Task(
            config=self.tasks_config['task_cyc_step_one_loop'],
            agent=self.cat_one(),
        )

    @task
    def task_step_five(self) -> Task:
        return Task(
            config=self.tasks_config['task_step_five'],
            agent=self.cat_one(),
        )

    @task
    def task_br_step_five(self) -> Task:
        return Task(
            config=self.tasks_config['task_br_step_five'],
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
