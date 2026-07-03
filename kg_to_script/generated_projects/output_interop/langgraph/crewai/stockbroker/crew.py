"""
Auto-generated CrewAI Crew: TradingSystem

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Provide portfolio overview and enable executing trades via the UI.
Capabilities:
  - : Execute market buy orders for a specified ticker and quantity at the provided price.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: buy_stock_tool — unknown tool class "buyStockTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("buyStockTool")
def buy_stock_tool(*args, **kwargs) -> str:
    """Executes stock purchase orders when invoked by the UI. Expects a JSON content with purchaseDetails {"""
    return "buy_stock_tool result"




@CrewBase
class TradingSystem:
    """TradingSystem crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def trade_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trade_agent'],
            tools=[buy_stock_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def open_buy_ui_task(self) -> Task:
        return Task(
            config=self.tasks_config['open_buy_ui_task'],
            agent=self.trade_agent(),
        )

    @task
    def execute_purchase_task(self) -> Task:
        return Task(
            config=self.tasks_config['execute_purchase_task'],
            agent=self.trade_agent(),
        )

    @task
    def confirm_purchase_task(self) -> Task:
        return Task(
            config=self.tasks_config['confirm_purchase_task'],
            agent=self.trade_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the TradingSystem"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
