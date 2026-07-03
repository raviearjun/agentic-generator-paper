"""
Auto-generated CrewAI Crew: mastravnext

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Crawls a website and extracts markdown content for downstream processing.
  - : Generates OpenAPI specification fragments from documentation pages and merges them.
  - : Formats YAML, creates branch, commits files and opens a pull request on GitHub.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_site_crawl — unknown tool class "toolsitecrawl"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsitecrawl")
def tool_site_crawl(*args, **kwargs) -> str:
    """Crawl a website and extract the markdown content"""
    return "tool_site_crawl result"

# TODO: tool_generate_spec — unknown tool class "toolgeneratespec"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolgeneratespec")
def tool_generate_spec(*args, **kwargs) -> str:
    """Generate a spec from a website"""
    return "tool_generate_spec result"

# TODO: tool_add_to_github — unknown tool class "tooladdtogithub"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("tooladdtogithub")
def tool_add_to_github(*args, **kwargs) -> str:
    """Commit the spec to GitHub and create a PR"""
    return "tool_add_to_github result"




@CrewBase
class mastravnext:
    """mastravnext crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def openapi_spec_gen_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['openapi_spec_gen_agent'],
            tools=[tool_site_crawl, tool_generate_spec, tool_add_to_github],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_site_crawl_sync(self) -> Task:
        return Task(
            config=self.tasks_config['task_site_crawl_sync'],
        )

    @task
    def task_add_to_github(self) -> Task:
        return Task(
            config=self.tasks_config['task_add_to_github'],
            agent=self.openapi_spec_gen_agent(),
        )

    @task
    def task_generate_spec(self) -> Task:
        return Task(
            config=self.tasks_config['task_generate_spec'],
            agent=self.openapi_spec_gen_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the mastravnext"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
