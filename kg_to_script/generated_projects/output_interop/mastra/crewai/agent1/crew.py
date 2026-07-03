"""
Auto-generated CrewAI Crew: MastraClientSystem

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Goal for the Mastra agent client: handle streaming responses, orchestrate client tool execution, and expose voice and observation endpoints.
  - : Provide stable streaming, tool execution continuation, and observability integration for agent runs.
Capabilities:
  - : Capability to synthesize audio from text.
  - : Capability to transcribe audio to text.
  - : Capability to execute a client-supplied tool via `clientTool.execute` and return results to the agent stream.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: voice_provider_tool — unknown tool class "VoiceProviderTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("VoiceProviderTool")
def voice_provider_tool(*args, **kwargs) -> str:
    """Voice provider used by the agent for text-to-speech (speak) and speech-to-text (listen) operations v"""
    return "voice_provider_tool result"

# TODO: client_tools_tool — unknown tool class "ClientToolsTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ClientToolsTool")
def client_tools_tool(*args, **kwargs) -> str:
    """Abstract representation of the `clientTools` map supplied to the Mastra agent client; client-provide"""
    return "client_tools_tool result"




@CrewBase
class MastraClientSystem:
    """MastraClientSystem crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def mastra_agent_client(self) -> Agent:
        return Agent(
            config=self.agents_config['mastra_agent_client'],
            tools=[voice_provider_tool, client_tools_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_process_request(self) -> Task:
        return Task(
            config=self.tasks_config['task_process_request'],
            agent=self.mastra_agent_client(),
        )

    @task
    def task_execute_client_tool(self) -> Task:
        return Task(
            config=self.tasks_config['task_execute_client_tool'],
            agent=self.mastra_agent_client(),
        )

    @task
    def task_return_response(self) -> Task:
        return Task(
            config=self.tasks_config['task_return_response'],
            agent=self.mastra_agent_client(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MastraClientSystem"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
