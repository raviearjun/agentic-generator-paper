"""
Auto-generated CrewAI Crew: CopyCrewagentsforcopygeneration

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Produce thorough product and competitor analysis to inform marketing strategy.
  - : Formulate marketing strategies and creative ideas based on product and competitor analysis.
  - : Produce multiple Instagram ad copy options aligned with campaign strategy.
  - : Generate three photographic concepts that best represent the campaign and product without showing the actual product.
  - : Ensure final creative outputs are aligned with product goals; review and approve imagery.
  - : Produce marketing analysis and 3 Instagram ad copy options for the product.
  - : Produce three photograph concepts and a reviewed final selection aligned with campaign copy.
Capabilities:
  - : Extract and summarize HTML content from websites.
  - : Query web search API and return ranked result snippets.
  - : Search Instagram content via web search for post examples and snippets.
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_scrape_website — unknown tool class "ToolScrapeWebsite"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolScrapeWebsite")
def tool_scrape_website(*args, **kwargs) -> str:
    """Scrapes a webpage via Browserless API and summarizes chunks using an LLM."""
    return "tool_scrape_website result"

# TODO: tool_search_internet — unknown tool class "ToolSearchInternet"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSearchInternet")
def tool_search_internet(*args, **kwargs) -> str:
    """Performs web searches using the Serper (google.serper.dev) API and returns top results."""
    return "tool_search_internet result"

# TODO: tool_search_instagram — unknown tool class "ToolSearchInstagram"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSearchInstagram")
def tool_search_instagram(*args, **kwargs) -> str:
    """Performs targeted Instagram site searches (site:instagram.com ...) via Serper API."""
    return "tool_search_instagram result"


# ===========================================================
# Custom LLM
# ===========================================================
product_competitor_agent_llm = LLM(model="ollama/model")
strategy_planner_agent_llm = LLM(model="ollama/model")
creative_content_creator_agent_llm = LLM(model="ollama/model")
senior_photographer_agent_llm = LLM(model="ollama/model")
chief_creative_diretor_agent_llm = LLM(model="ollama/model")


@CrewBase
class CopyCrewagentsforcopygeneration:
    """CopyCrewagentsforcopygeneration crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def product_competitor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['product_competitor_agent'],
            tools=[tool_scrape_website, tool_search_internet],
            llm=product_competitor_agent_llm,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def strategy_planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['strategy_planner_agent'],
            tools=[tool_scrape_website, tool_search_internet, tool_search_instagram],
            llm=strategy_planner_agent_llm,
            verbose=True,
        )

    @agent
    def creative_content_creator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_content_creator_agent'],
            tools=[tool_scrape_website, tool_search_internet, tool_search_instagram],
            llm=creative_content_creator_agent_llm,
            verbose=True,
        )

    @agent
    def senior_photographer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_photographer_agent'],
            tools=[tool_scrape_website, tool_search_internet, tool_search_instagram],
            llm=senior_photographer_agent_llm,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def chief_creative_diretor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_creative_diretor_agent'],
            tools=[tool_scrape_website, tool_search_internet, tool_search_instagram],
            llm=chief_creative_diretor_agent_llm,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_product_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['task_product_analysis'],
            agent=self.product_competitor_agent(),
        )

    @task
    def task_take_photograph(self) -> Task:
        return Task(
            config=self.tasks_config['task_take_photograph'],
            agent=self.senior_photographer_agent(),
        )

    @task
    def task_competitor_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['task_competitor_analysis'],
            agent=self.product_competitor_agent(),
        )

    @task
    def task_review_photo(self) -> Task:
        return Task(
            config=self.tasks_config['task_review_photo'],
            agent=self.chief_creative_diretor_agent(),
        )

    @task
    def task_campaign_development(self) -> Task:
        return Task(
            config=self.tasks_config['task_campaign_development'],
            agent=self.strategy_planner_agent(),
        )

    @task
    def task_instagram_ad_copy(self) -> Task:
        return Task(
            config=self.tasks_config['task_instagram_ad_copy'],
            agent=self.creative_content_creator_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the CopyCrewagentsforcopygeneration"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
