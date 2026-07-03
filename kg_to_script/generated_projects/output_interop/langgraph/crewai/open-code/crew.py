"""
Auto-generated CrewAI Crew: ProposedChangeUITeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Facilitate safe review and application of code changes via an agent-mediated user workflow.
Human Agents:
  - human_user ()
Capabilities:
  - : Apply proposed file changes / update repository file contents.
  - : Capability enabling the agent to request file updates via external tool calls.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_update_file — unknown tool class "Toolupdatefile"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("Toolupdatefile")
def tool_update_file(*args, **kwargs) -> str:
    """Tool used to apply an accepted proposed change to files (invoked via tool call messages)."""
    return "tool_update_file result"




@CrewBase
class ProposedChangeUITeam:
    """ProposedChangeUITeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def langgraph_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['langgraph_agent'],
            tools=[tool_update_file],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_propose_change(self) -> Task:
        return Task(
            config=self.tasks_config['task_propose_change'],
            agent=self.langgraph_agent(),
        )

    @task
    def task_user_decision(self) -> Task:
        return Task(
            config=self.tasks_config['task_user_decision'],
            human_input=True,
        )

    @task
    def task_handle_accept(self) -> Task:
        return Task(
            config=self.tasks_config['task_handle_accept'],
            agent=self.langgraph_agent(),
        )

    @task
    def task_handle_reject(self) -> Task:
        return Task(
            config=self.tasks_config['task_handle_reject'],
            agent=self.langgraph_agent(),
        )

    @task
    def task_finalize_ui(self) -> Task:
        return Task(
            config=self.tasks_config['task_finalize_ui'],
            agent=self.langgraph_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the ProposedChangeUITeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
