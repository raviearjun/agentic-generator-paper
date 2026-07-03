"""
Auto-generated CrewAI Crew: MastraInstancelocal

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Executes the tool's registered logic (no input schema required)
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: my_tool — unknown tool class "mytool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("mytool")
def my_tool(*args, **kwargs) -> str:
    """My tool description"""
    return "my_tool result"




@CrewBase
class MastraInstancelocal:
    """MastraInstancelocal crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def chef_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chef_agent'],
            tools=[my_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_query_pantry(self) -> Task:
        return Task(
            config=self.tasks_config['task_query_pantry'],
            agent=self.chef_agent(),
        )

    @task
    def task_generate_text(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_text'],
            agent=self.chef_agent(),
        )

    @task
    def task_text_stream(self) -> Task:
        return Task(
            config=self.tasks_config['task_text_stream'],
            agent=self.chef_agent(),
        )

    @task
    def task_generate_stream(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_stream'],
            agent=self.chef_agent(),
        )

    @task
    def task_text_object(self) -> Task:
        return Task(
            config=self.tasks_config['task_text_object'],
            agent=self.chef_agent(),
        )

    @task
    def task_text_object_jsonschema(self) -> Task:
        return Task(
            config=self.tasks_config['task_text_object_jsonschema'],
            agent=self.chef_agent(),
        )

    @task
    def task_generate_object(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_object'],
            agent=self.chef_agent(),
        )

    @task
    def task_stream_object(self) -> Task:
        return Task(
            config=self.tasks_config['task_stream_object'],
            agent=self.chef_agent(),
        )

    @task
    def task_generate_stream_object(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_stream_object'],
            agent=self.chef_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MastraInstancelocal"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
