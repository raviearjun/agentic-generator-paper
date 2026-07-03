"""
Auto-generated CrewAI Crew: teamexpandidea

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Understand and expand upon the essence of ideas, make sure they are great and focus on real pain points others could benefit from.
  - : Craft compelling stories using the Golden Circle method to captivate and engage people around an idea.
  - : Build an intuitive, aesthetically pleasing, and high-converting landing page.
  - : Ensure the landing page content is clear, concise, and captivating.
Capabilities:
  - : Perform web search queries and return structured results.
  - : Scrape website HTML and summarize content into concise summaries.
  - : Inspect available landing page templates and surface options.
  - : Copy a landing page template folder into the working project directory.
  - : Write files to the workdir with validation and allowed extensions.
  - : Read files from the workdir.
  - : List directory contents under the workdir.
Resources:
  - : Extraction created LLMAgent, Tool, Task, WorkflowPattern, WorkflowStep, Prompt, Goal, Config, and LanguageModel individuals per CrewAI mapping. Assumed default model 'gpt-4'.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_search_internet — unknown tool class "toolsearchinternet"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolsearchinternet")
def tool_search_internet(*args, **kwargs) -> str:
    """Search the internet using Serper Dev API and return organic results."""
    return "tool_search_internet result"

# TODO: tool_scrape_and_summarize_website — unknown tool class "toolscrapeandsummarizewebsite"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolscrapeandsummarizewebsite")
def tool_scrape_and_summarize_website(*args, **kwargs) -> str:
    """Scrape website content via Browserless and summarize chunks using internal agent tasks."""
    return "tool_scrape_and_summarize_website result"

# TODO: tool_learn_landing_page_options — unknown tool class "toollearnlandingpageoptions"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toollearnlandingpageoptions")
def tool_learn_landing_page_options(*args, **kwargs) -> str:
    """Read templates configuration and surface available landing page templates."""
    return "tool_learn_landing_page_options result"

# TODO: tool_copy_landing_page_template — unknown tool class "toolcopylandingpagetemplate"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolcopylandingpagetemplate")
def tool_copy_landing_page_template(*args, **kwargs) -> str:
    """Copy a selected landing page template folder from templates/ into workdir/."""
    return "tool_copy_landing_page_template result"

# TODO: tool_write_file — unknown tool class "toolwritefile"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolwritefile")
def tool_write_file(*args, **kwargs) -> str:
    """Validated write file tool that writes React component and other files into workdir."""
    return "tool_write_file result"

# TODO: tool_read_file — unknown tool class "toolreadfile"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolreadfile")
def tool_read_file(*args, **kwargs) -> str:
    """Read file from the toolkit root_dir (workdir)."""
    return "tool_read_file result"

# TODO: tool_list_directory — unknown tool class "toollistdirectory"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toollistdirectory")
def tool_list_directory(*args, **kwargs) -> str:
    """List directory contents from the toolkit root_dir (workdir)."""
    return "tool_list_directory result"




@CrewBase
class teamexpandidea:
    """teamexpandidea crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def senior_idea_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_idea_analyst'],
            tools=[tool_search_internet, tool_scrape_and_summarize_website],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def senior_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_strategist'],
            tools=[tool_search_internet, tool_scrape_and_summarize_website],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def senior_react_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_react_engineer'],
            tools=[tool_search_internet, tool_scrape_and_summarize_website, tool_learn_landing_page_options, tool_copy_landing_page_template, tool_write_file, tool_read_file, tool_list_directory],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def senior_content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_content_editor'],
            tools=[tool_write_file],
            allow_delegation=False,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_expand_idea(self) -> Task:
        return Task(
            config=self.tasks_config['task_expand_idea'],
            agent=self.senior_idea_analyst(),
        )

    @task
    def task_choose_template(self) -> Task:
        return Task(
            config=self.tasks_config['task_choose_template'],
            agent=self.senior_react_engineer(),
        )

    @task
    def task_component_content(self) -> Task:
        return Task(
            config=self.tasks_config['task_component_content'],
            agent=self.senior_content_editor(),
        )

    @task
    def task_refine_idea(self) -> Task:
        return Task(
            config=self.tasks_config['task_refine_idea'],
            agent=self.senior_strategist(),
        )

    @task
    def task_update_page(self) -> Task:
        return Task(
            config=self.tasks_config['task_update_page'],
            agent=self.senior_react_engineer(),
        )

    @task
    def task_update_component(self) -> Task:
        return Task(
            config=self.tasks_config['task_update_component'],
            agent=self.senior_content_editor(),
        )

    @task
    def task_qa_component(self) -> Task:
        return Task(
            config=self.tasks_config['task_qa_component'],
            agent=self.senior_content_editor(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the teamexpandidea"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
