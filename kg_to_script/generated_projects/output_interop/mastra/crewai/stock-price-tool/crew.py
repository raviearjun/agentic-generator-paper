"""
Auto-generated CrewAI Crew: mastrainstance

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Fetch last day's closing stock price for a given symbol
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: stock_prices_tool — unknown tool class "stockPricesTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("stockPricesTool")
def stock_prices_tool(*args, **kwargs) -> str:
    """Fetches the last day's closing stock price for a given symbol"""
    return "stock_prices_tool result"




@CrewBase
class mastrainstance:
    """mastrainstance crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def stock_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_agent'],
            tools=[stock_prices_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_init(self) -> Task:
        return Task(
            config=self.tasks_config['task_init'],
            agent=self.stock_agent(),
        )

    @task
    def task_query(self) -> Task:
        return Task(
            config=self.tasks_config['task_query'],
            agent=self.stock_agent(),
        )

    @task
    def task_tool_call(self) -> Task:
        return Task(
            config=self.tasks_config['task_tool_call'],
            agent=self.stock_agent(),
        )

    @task
    def task_end(self) -> Task:
        return Task(
            config=self.tasks_config['task_end'],
            agent=self.stock_agent(),
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
