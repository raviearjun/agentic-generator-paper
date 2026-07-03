"""
Auto-generated CrewAI Crew: StockAnalysisCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Automate the process of analyzing a stock to produce a detailed report and investment recommendation.
Capabilities:
  - : Performs arithmetic and mathematical calculations.
  - : Scrapes and summarizes web page content.
  - : Performs web searches and retrieves relevant results.
  - : Searches textual sources or indexes.
  - : Semantic search within a company's 10-K filing content.
  - : Semantic search within a company's 10-Q filing content.
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_calculator_tool — unknown tool class "ToolCalculatorTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolCalculatorTool")
def tool_calculator_tool(*args, **kwargs) -> str:
    """Performs safe mathematical expression evaluation (add, sub, mul, div, pow, mod)."""
    return "tool_calculator_tool result"

# TODO: tool_scrape_website_tool — unknown tool class "ToolScrapeWebsiteTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolScrapeWebsiteTool")
def tool_scrape_website_tool(*args, **kwargs) -> str:
    """Tool to scrape website content and convert to text for summarization."""
    return "tool_scrape_website_tool result"

# TODO: tool_website_search_tool — unknown tool class "ToolWebsiteSearchTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolWebsiteSearchTool")
def tool_website_search_tool(*args, **kwargs) -> str:
    """Tool to search the web for relevant pages and summaries."""
    return "tool_website_search_tool result"

# TODO: tool_txt_search_tool — unknown tool class "ToolTXTSearchTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolTXTSearchTool")
def tool_txt_search_tool(*args, **kwargs) -> str:
    """Text search tool for searching indexed textual data."""
    return "tool_txt_search_tool result"

# TODO: tool_sec10_k_tool_generic — unknown tool class "ToolSEC10KToolGeneric"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSEC10KToolGeneric")
def tool_sec10_k_tool_generic(*args, **kwargs) -> str:
    """A tool to semantically search a company's latest 10-K SEC filing content."""
    return "tool_sec10_k_tool_generic result"

# TODO: tool_sec10_q_tool_generic — unknown tool class "ToolSEC10QToolGeneric"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSEC10QToolGeneric")
def tool_sec10_q_tool_generic(*args, **kwargs) -> str:
    """A tool to semantically search a company's latest 10-Q SEC filing content."""
    return "tool_sec10_q_tool_generic result"

# TODO: tool_sec10_k_tool_amzn — unknown tool class "ToolSEC10KToolAMZN"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSEC10KToolAMZN")
def tool_sec10_k_tool_amzn(*args, **kwargs) -> str:
    """SEC10KTool initialized with stock_name=AMZN to pre-load AMZN latest 10-K content."""
    return "tool_sec10_k_tool_amzn result"

# TODO: tool_sec10_q_tool_amzn — unknown tool class "ToolSEC10QToolAMZN"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSEC10QToolAMZN")
def tool_sec10_q_tool_amzn(*args, **kwargs) -> str:
    """SEC10QTool initialized with stock_name=AMZN to pre-load AMZN latest 10-Q content."""
    return "tool_sec10_q_tool_amzn result"


# ===========================================================
# Custom LLM
# ===========================================================
financial_agent_llm = LLM(model="ollama/local")
research_analyst_agent_llm = LLM(model="ollama/local")
financial_analyst_agent_llm = LLM(model="ollama/local")
investment_advisor_agent_llm = LLM(model="ollama/local")


@CrewBase
class StockAnalysisCrew:
    """StockAnalysisCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def financial_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_agent'],
            tools=[tool_calculator_tool, tool_scrape_website_tool, tool_website_search_tool, tool_sec10_k_tool_amzn, tool_sec10_q_tool_amzn],
            llm=financial_agent_llm,
            verbose=True,
        )

    @agent
    def research_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst_agent'],
            tools=[tool_scrape_website_tool, tool_sec10_k_tool_amzn, tool_sec10_q_tool_amzn],
            llm=research_analyst_agent_llm,
            verbose=True,
        )

    @agent
    def financial_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst_agent'],
            tools=[tool_calculator_tool, tool_scrape_website_tool, tool_website_search_tool, tool_sec10_k_tool_generic, tool_sec10_q_tool_generic],
            llm=financial_analyst_agent_llm,
            verbose=True,
        )

    @agent
    def investment_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor_agent'],
            tools=[tool_calculator_tool, tool_scrape_website_tool, tool_website_search_tool],
            llm=investment_advisor_agent_llm,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_financial_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['task_financial_analysis'],
            agent=self.financial_analyst_agent(),
        )

    @task
    def task_research(self) -> Task:
        return Task(
            config=self.tasks_config['task_research'],
            agent=self.research_analyst_agent(),
        )

    @task
    def task_filings_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['task_filings_analysis'],
            agent=self.financial_analyst_agent(),
        )

    @task
    def task_recommend(self) -> Task:
        return Task(
            config=self.tasks_config['task_recommend'],
            agent=self.investment_advisor_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the StockAnalysisCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
