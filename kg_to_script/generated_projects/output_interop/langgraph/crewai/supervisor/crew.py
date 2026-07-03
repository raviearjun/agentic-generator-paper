"""
Auto-generated CrewAI Crew: GenerativeUIAgent

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Fetch price, buy/sell tickers, retrieve user portfolio.
  - : Suggest restaurants, hotels, and itineraries for locations.
  - : Generate project code (React TODO app) and related files.
  - : Place pizza orders and return confirmation details.
  - : Generate long-form text documents or writing deliverables.
  - : Select the appropriate target route/tool based on user input.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_stockbroker — unknown tool class "toolstockbroker"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolstockbroker")
def tool_stockbroker(*args, **kwargs) -> str:
    """can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio"""
    return "tool_stockbroker result"

# TODO: tool_trip_planner — unknown tool class "tooltripPlanner"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("tooltripPlanner")
def tool_trip_planner(*args, **kwargs) -> str:
    """helps the user plan their trip; can suggest restaurants and places to stay in any given location."""
    return "tool_trip_planner result"

# TODO: tool_open_code — unknown tool class "toolopenCode"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolopenCode")
def tool_open_code(*args, **kwargs) -> str:
    """can write a React TODO app for the user. Only call this tool if they request a TODO app."""
    return "tool_open_code result"

# TODO: tool_order_pizza — unknown tool class "toolorderPizza"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolorderPizza")
def tool_order_pizza(*args, **kwargs) -> str:
    """can order a pizza for the user"""
    return "tool_order_pizza result"

# TODO: tool_writer_agent — unknown tool class "toolwriterAgent"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolwriterAgent")
def tool_writer_agent(*args, **kwargs) -> str:
    """can write a text document for the user. Only call this tool if they request a text document."""
    return "tool_writer_agent result"

# TODO: tool_router — unknown tool class "toolrouter"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolrouter")
def tool_router(*args, **kwargs) -> str:
    """A tool to route the user's query to the appropriate tool. (Used as a tool schema bound to the routin"""
    return "tool_router result"




@CrewBase
class GenerativeUIAgent:
    """GenerativeUIAgent crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def supervisor(self) -> Agent:
        return Agent(
            config=self.agents_config['supervisor'],
            tools=[tool_stockbroker, tool_trip_planner, tool_open_code, tool_order_pizza, tool_writer_agent, tool_router],
        )

    @agent
    def router(self) -> Agent:
        return Agent(
            config=self.agents_config['router'],
            tools=[tool_router],
        )

    @agent
    def general_input(self) -> Agent:
        return Agent(
            config=self.agents_config['general_input'],
            tools=[tool_stockbroker, tool_trip_planner, tool_open_code, tool_order_pizza, tool_writer_agent],
        )

    @agent
    def stockbroker(self) -> Agent:
        return Agent(
            config=self.agents_config['stockbroker'],
            tools=[tool_stockbroker],
        )

    @agent
    def trip_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['trip_planner'],
            tools=[tool_trip_planner],
        )

    @agent
    def open_code(self) -> Agent:
        return Agent(
            config=self.agents_config['open_code'],
            tools=[tool_open_code],
        )

    @agent
    def order_pizza(self) -> Agent:
        return Agent(
            config=self.agents_config['order_pizza'],
            tools=[tool_order_pizza],
        )

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            tools=[tool_writer_agent],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_start(self) -> Task:
        return Task(
            config=self.tasks_config['task_start'],
            agent=self.supervisor(),
        )

    @task
    def task_router(self) -> Task:
        return Task(
            config=self.tasks_config['task_router'],
            agent=self.router(),
        )

    @task
    def task_general_input(self) -> Task:
        return Task(
            config=self.tasks_config['task_general_input'],
            agent=self.general_input(),
        )

    @task
    def task_stockbroker(self) -> Task:
        return Task(
            config=self.tasks_config['task_stockbroker'],
            agent=self.stockbroker(),
        )

    @task
    def task_trip_planner(self) -> Task:
        return Task(
            config=self.tasks_config['task_trip_planner'],
            agent=self.trip_planner(),
        )

    @task
    def task_open_code(self) -> Task:
        return Task(
            config=self.tasks_config['task_open_code'],
            agent=self.open_code(),
        )

    @task
    def task_order_pizza(self) -> Task:
        return Task(
            config=self.tasks_config['task_order_pizza'],
            agent=self.order_pizza(),
        )

    @task
    def task_writer_agent(self) -> Task:
        return Task(
            config=self.tasks_config['task_writer_agent'],
            agent=self.writer_agent(),
        )

    @task
    def task_end(self) -> Task:
        return Task(
            config=self.tasks_config['task_end'],
            agent=self.supervisor(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the GenerativeUIAgent"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
