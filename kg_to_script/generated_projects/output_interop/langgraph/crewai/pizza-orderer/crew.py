"""
Auto-generated CrewAI Crew: OrderPizzaGraphTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : High-level goal to find a pizza shop and place an order for the user.
Capabilities:
  - : Find nearby pizza shop and return contact details (address, phone).
  - : Place an order at the specified pizza shop and return order confirmation.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: find_pizza_tool — unknown tool class "FindPizzaTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("FindPizzaTool")
def find_pizza_tool(*args, **kwargs) -> str:
    """Tool invoked to search for a pizza shop and return address and phone number."""
    return "find_pizza_tool result"

# TODO: place_order_tool — unknown tool class "PlaceOrderTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("PlaceOrderTool")
def place_order_tool(*args, **kwargs) -> str:
    """Tool invoked to place a pizza order and confirm success."""
    return "place_order_tool result"




@CrewBase
class OrderPizzaGraphTeam:
    """OrderPizzaGraphTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def langgraph_anthropic_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['langgraph_anthropic_agent'],
            tools=[find_pizza_tool, place_order_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def find_store_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_store_task'],
            agent=self.langgraph_anthropic_agent(),
        )

    @task
    def order_pizza_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_pizza_task'],
            agent=self.langgraph_anthropic_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the OrderPizzaGraphTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
