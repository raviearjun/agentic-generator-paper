"""
Auto-generated CrewAI Crew: EmailAssistantTeamStateGraphsystem

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Human Agents:
  - human_user ()
Capabilities:
  - : Produces an email object with subject, body, and recipient based on conversation history or user edits.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_write_email — unknown tool class "Toolwriteemail"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("Toolwriteemail")
def tool_write_email(*args, **kwargs) -> str:
    """Write an email based on the conversation history"""
    return "tool_write_email result"




@CrewBase
class EmailAssistantTeamStateGraphsystem:
    """EmailAssistantTeamStateGraphsystem crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def email_assistant_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['email_assistant_agent'],
            tools=[tool_write_email],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_write_email(self) -> Task:
        return Task(
            config=self.tasks_config['task_write_email'],
            agent=self.email_assistant_agent(),
        )

    @task
    def task_interrupt(self) -> Task:
        return Task(
            config=self.tasks_config['task_interrupt'],
            human_input=True,
        )

    @task
    def task_rewrite_email(self) -> Task:
        return Task(
            config=self.tasks_config['task_rewrite_email'],
            agent=self.email_assistant_agent(),
        )

    @task
    def task_send_email(self) -> Task:
        return Task(
            config=self.tasks_config['task_send_email'],
            agent=self.email_assistant_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the EmailAssistantTeamStateGraphsystem"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
