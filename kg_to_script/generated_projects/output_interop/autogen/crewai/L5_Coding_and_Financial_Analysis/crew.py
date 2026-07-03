"""
Auto-generated CrewAI Crew: CodingandFinancialAnalysisCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Produce and save plots (e.g., ytd_stock_gains.png, stock_prices_YTD_plot.png) showing year-to-date gains for requested tickers (NVDA and TSLA/TLSA).
Capabilities:
  - : Ability to execute arbitrary code snippets in a sandboxed local environment.
  - : Download historical stock close prices for given symbols and date range.
  - : Render time series plots for stock price data and save to image files.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_local_cli_executor — unknown tool class "toollocalcliexecutor"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toollocalcliexecutor")
def tool_local_cli_executor(*args, **kwargs) -> str:
    """Executor used to run code locally with a working directory and timeout; can register functions to be"""
    return "tool_local_cli_executor result"

# TODO: tool_get_stock_prices — unknown tool class "toolgetstockprices"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolgetstockprices")
def tool_get_stock_prices(*args, **kwargs) -> str:
    """Function that downloads stock prices using yfinance and returns closing prices for given symbols bet"""
    return "tool_get_stock_prices result"

# TODO: tool_plot_stock_prices — unknown tool class "toolplotstockprices"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolplotstockprices")
def tool_plot_stock_prices(*args, **kwargs) -> str:
    """Function that plots provided stock prices dataframe and saves the figure to a specified filename usi"""
    return "tool_plot_stock_prices result"




@CrewBase
class CodingandFinancialAnalysisCrew:
    """CodingandFinancialAnalysisCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def code_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_writer_agent'],
        )

    @agent
    def code_executor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_executor_agent'],
            tools=[tool_local_cli_executor, tool_get_stock_prices, tool_plot_stock_prices],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_plot_ytd_v1(self) -> Task:
        return Task(
            config=self.tasks_config['task_plot_ytd_v1'],
            agent=self.code_executor_agent(),
        )

    @task
    def task_plot_ytd_v2(self) -> Task:
        return Task(
            config=self.tasks_config['task_plot_ytd_v2'],
            agent=self.code_executor_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the CodingandFinancialAnalysisCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
