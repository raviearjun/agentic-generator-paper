"""
Auto-generated CrewAI Crew: MyCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Select the best city based on weather patterns, seasonal events, and travel costs
  - : Provide in-depth local guide content, hidden gems, and practical tips.
  - : Create a 7-day travel itinerary with detailed daily plans, budgets, packing suggestions, and logistics.
Capabilities:
  - : Analyze and compare cities by weather conditions, events, and travel costs; deliver a detailed city selection report.
  - : Collect and synthesize local cultural, tourism and attraction information into a comprehensive guide.
  - : Generate optimized daily travel itineraries with logistics, budget calculations, and packing recommendations.
  - : Search the internet for relevant results and return structured snippets with title, link, and snippet text.
  - : Scrape raw HTML of a website, partition and summarize content with an internal summarization agent; returns concise summaries for each chunk.
  - : Perform safe arithmetic evaluation of mathematical expressions (supports + - * / % ** and parentheses). Returns numeric result or error message.
Resources:
  - : Used by SearchTools.search_internet to obtain organic search results.
  - : Used by BrowserTools.scrape_and_summarize_website to fetch HTML content.
  - : API key used by the language model client OpenAI (langchain_openai.OpenAI).
  - : The final produced travel plan (7-day itinerary), including hotels, restaurants, per-day schedule, weather forecast, packing suggestions, and budget breakdown.
  - : Comprehensive city guide including hidden gems, cultural hotspots and practical tips.
  - : Detailed report on chosen city including flight costs, weather forecast, and attractions.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: search_tools — unknown tool class "searchtools"
#   Description: Toolset providing search_internet(query) which posts to Serper API and returns t
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# search_tools = SomeCustomTool(SERPER_API_KEY="bc357b147050e86d66422d53e58d003af4188a18")
# TODO: browser_tools — unknown tool class "browsertools"
#   Description: Scrape website content using Browserless content API; partitions HTML and produc
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# browser_tools = SomeCustomTool(BROWSERLESS_API_KEY="2TVmWmGeQ9ziDXq4bcbbb03e8ff6ea65f0e6de71db1498ce5")
# TODO: calculator_tools — unknown tool class "calculatortools"
#   Description: Make a calculation(operation) evaluates basic arithmetic expressions safely usin
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# calculator_tools = SomeCustomTool()



@CrewBase
class MyCrew:
    """MyCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def city_selection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selection_agent'],
            tools=[search_tools, browser_tools],
        )

    @agent
    def local_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert_agent'],
            tools=[search_tools, browser_tools],
        )

    @agent
    def travel_concierge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge_agent'],
            tools=[search_tools, browser_tools, calculator_tools],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def identify_task(self) -> Task:
        return Task(
            config=self.tasks_config['identify_task'],
            agent=self.city_selection_agent(),
        )

    @task
    def gather_task(self) -> Task:
        return Task(
            config=self.tasks_config['gather_task'],
            agent=self.local_expert_agent(),
        )

    @task
    def plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['plan_task'],
            agent=self.travel_concierge_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MyCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
