"""
Auto-generated CrewAI Crew: MarkDownValidatorCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Provide a detailed list of the markdown linting results.
Give a summary with actionable tasks to address the validation results.
Write your response as if you were handing it to a developer to fix the issues.
DO NOT provide examples of how to fix the issues or recommend other tools to use.
Capabilities:
  - : Identify markdown syntax issues using pymarkdown, returning formatted scan failures (file, line, rule, description).
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: markdown_validation_tool — unknown tool class "markdownvalidationtool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("markdownvalidationtool")
def markdown_validation_tool(*args, **kwargs) -> str:
    """A tool to review files for markdown syntax errors. Uses PyMarkdownApi to scan a file path and return"""
    return "markdown_validation_tool result"




@CrewBase
class MarkDownValidatorCrew:
    """MarkDownValidatorCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def requirements_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_manager'],
            tools=[markdown_validation_tool],
            allow_delegation=False,
            verbose=False,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def syntax_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['syntax_review_task'],
            agent=self.requirements_manager(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MarkDownValidatorCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
