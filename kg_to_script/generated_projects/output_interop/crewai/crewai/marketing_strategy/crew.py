"""
Auto-generated CrewAI Crew: MarketingPostsCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Create a comprehensive marketing strategy to showcase CrewAI's AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities, targeting enterprise decision-makers.
  - : Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.
  - : Synthesize amazing insights from product analysis to formulate incredible marketing strategies.
  - : Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact ad copies.
Capabilities:
  - : Perform web search queries and return relevant search results.
  - : Retrieve and parse website content for analysis.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_serper_dev_tool — unknown tool class "toolSerperDevTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolSerperDevTool")
def tool_serper_dev_tool(*args, **kwargs) -> str:
    """Tool for performing web/search queries via Serper.dev (used to find up-to-date information)."""
    return "tool_serper_dev_tool result"

# TODO: tool_scrape_website_tool — unknown tool class "toolScrapeWebsiteTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolScrapeWebsiteTool")
def tool_scrape_website_tool(*args, **kwargs) -> str:
    """Tool to scrape website content for extracting information about customers and competitors."""
    return "tool_scrape_website_tool result"




@CrewBase
class MarketingPostsCrew:
    """MarketingPostsCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def lead_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_market_analyst'],
            tools=[tool_serper_dev_tool, tool_scrape_website_tool],
            verbose=True,
        )

    @agent
    def chief_marketing_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_marketing_strategist'],
            tools=[tool_serper_dev_tool, tool_scrape_website_tool],
            verbose=True,
        )

    @agent
    def creative_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_content_creator'],
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_research(self) -> Task:
        return Task(
            config=self.tasks_config['task_research'],
            agent=self.lead_market_analyst(),
        )

    @task
    def task_project_understanding(self) -> Task:
        return Task(
            config=self.tasks_config['task_project_understanding'],
            agent=self.chief_marketing_strategist(),
        )

    @task
    def task_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['task_marketing_strategy'],
            agent=self.chief_marketing_strategist(),
        )

    @task
    def task_campaign_idea(self) -> Task:
        return Task(
            config=self.tasks_config['task_campaign_idea'],
            agent=self.creative_content_creator(),
        )

    @task
    def task_copy_creation(self) -> Task:
        return Task(
            config=self.tasks_config['task_copy_creation'],
            agent=self.creative_content_creator(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MarketingPostsCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
