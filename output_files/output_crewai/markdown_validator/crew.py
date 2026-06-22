"""
Auto-generated CrewAI Crew: MarkDownValidatorCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - Markdown validation crew goal: Provide a detailed list of the markdown linting results. Give a summary with actionable tasks to address the validation results. Write your response as if you were handing it to a developer to fix the issues. DO NOT provide examples of how to fix the issues or recommend other tools to use.
  - Requirements Manager goal: Provide a detailed list of the markdown linting results. Give a summary with actionable tasks to address the validation results. Write your response as if you were handing it to a developer to fix the issues. DO NOT provide examples of how to fix the issues or recommend other tools to use.
Resources:
  - Markdown validation report (tool output): Formatted string of validation results returned by markdown_validation_tool. Example output forms: 'No markdown validation issues found.' or a newline-separated list of detected rule violations with file, line, rule id, rule name and description.
  - PyMarkdownApi: The PyMarkdownApi library instance invoked by the tool implementation. The tool calls PyMarkdownApi().scan_path(file_path) to perform the scan and returns a formatted summary.
  - Input markdown file (CLI filename): The file path provided via command-line to the CLI (sys.argv[1] when running). The task expects only the file path string (filename) to be passed to the markdown_validation_tool.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: markdown_validation_tool — unknown tool class "markdownvalidationtool"
#   Description: Tool definition (from src/markdown_validator/tools/markdownTools.py):
- Tool nam
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# markdown_validation_tool = SomeCustomTool(tool_registration_name="markdown_validation_tool")



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
