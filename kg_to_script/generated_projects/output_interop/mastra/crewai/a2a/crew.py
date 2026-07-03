"""
Auto-generated CrewAI Crew: MastraA2AClient

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - : Capabilities to send/receive messages, manage tasks, and configure push notifications via A2A JSON-RPC.
  - : Process and deserialize server-sent A2A event streams into application-level event objects.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_a2_a_api — unknown tool class "ToolA2AAPI"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolA2AAPI")
def tool_a2_a_api(*args, **kwargs) -> str:
    """A2A JSON-RPC HTTP API endpoints used to interact with remote agents (agent-card, message/send, messa"""
    return "tool_a2_a_api result"

# TODO: tool_process_a2_a_stream — unknown tool class "ToolProcessA2AStream"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolProcessA2AStream")
def tool_process_a2_a_stream(*args, **kwargs) -> str:
    """Utility to parse and yield typed A2A stream events (SSE -> typed Message/Task/TaskStatusUpdateEvent/"""
    return "tool_process_a2_a_stream result"




@CrewBase
class MastraA2AClient:
    """MastraA2AClient crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def agent_id_constructor_parameter(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_id_constructor_parameter'],
            tools=[tool_a2_a_api, tool_process_a2_a_stream],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_get_agent_card(self) -> Task:
        return Task(
            config=self.tasks_config['task_get_agent_card'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_send_message(self) -> Task:
        return Task(
            config=self.tasks_config['task_send_message'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_send_message_stream(self) -> Task:
        return Task(
            config=self.tasks_config['task_send_message_stream'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_get_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_get_task'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_cancel_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_cancel_task'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_resubscribe_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_resubscribe_task'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_set_push_notification_config(self) -> Task:
        return Task(
            config=self.tasks_config['task_set_push_notification_config'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_get_push_notification_config(self) -> Task:
        return Task(
            config=self.tasks_config['task_get_push_notification_config'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_list_push_notification_config(self) -> Task:
        return Task(
            config=self.tasks_config['task_list_push_notification_config'],
            agent=self.agent_id_constructor_parameter(),
        )

    @task
    def task_delete_push_notification_config(self) -> Task:
        return Task(
            config=self.tasks_config['task_delete_push_notification_config'],
            agent=self.agent_id_constructor_parameter(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MastraA2AClient"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
