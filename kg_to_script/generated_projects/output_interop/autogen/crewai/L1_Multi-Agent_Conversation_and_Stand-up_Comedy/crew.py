"""
Auto-generated CrewAI Crew: StandupDuo

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Deliver a short comedic routine for the audience.
Capabilities:
  - : Provides LLM inference and chat functionality.
  - : Retrieves OpenAI API key from environment or secret store.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_open_ai_api — unknown tool class "ToolOpenAIAPI"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolOpenAIAPI")
def tool_open_ai_api(*args, **kwargs) -> str:
    """External LLM API used by ConversableAgent (via autogen/OpenAI client)."""
    return "tool_open_ai_api result"

# TODO: tool_get_openai_api_key — unknown tool class "Toolgetopenaiapikey"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("Toolgetopenaiapikey")
def tool_get_openai_api_key(*args, **kwargs) -> str:
    """Helper function used to retrieve the OpenAI API key from environment/config."""
    return "tool_get_openai_api_key result"




@CrewBase
class StandupDuo:
    """StandupDuo crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def chatbot(self) -> Agent:
        return Agent(
            config=self.agents_config['chatbot'],
            tools=[tool_open_ai_api, tool_get_openai_api_key],
        )

    @agent
    def unnamed(self) -> Agent:
        return Agent(
            config=self.agents_config['unnamed'],
            tools=[tool_open_ai_api],
        )

    @agent
    def unnamed(self) -> Agent:
        return Agent(
            config=self.agents_config['unnamed'],
            tools=[tool_open_ai_api],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_guodegang_initiate_chat_1(self) -> Task:
        return Task(
            config=self.tasks_config['task_guodegang_initiate_chat_1'],
            agent=self.unnamed(),
        )

    @task
    def task_guodegang_initiate_chat_2(self) -> Task:
        return Task(
            config=self.tasks_config['task_guodegang_initiate_chat_2'],
            agent=self.unnamed(),
        )

    @task
    def task_guodegang_send_followup(self) -> Task:
        return Task(
            config=self.tasks_config['task_guodegang_send_followup'],
            agent=self.unnamed(),
        )

    @task
    def task_chatbot_reply_1(self) -> Task:
        return Task(
            config=self.tasks_config['task_chatbot_reply_1'],
            agent=self.chatbot(),
        )

    @task
    def task_chatbot_reply_2(self) -> Task:
        return Task(
            config=self.tasks_config['task_chatbot_reply_2'],
            agent=self.chatbot(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the StandupDuo"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
