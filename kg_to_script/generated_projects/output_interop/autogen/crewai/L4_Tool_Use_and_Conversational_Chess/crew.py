"""
Auto-generated CrewAI Crew: ConversationalChessTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Team-level goal: have the agents play a game of chess via conversational tool calls.
Capabilities:
  - : Provides legal moves for the current chess position.
  - : Apply a move to the board and update board state; produce descriptive move result.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_get_legal_moves — unknown tool class "toolgetlegalmoves"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolgetlegalmoves")
def tool_get_legal_moves(*args, **kwargs) -> str:
    """Returns a list of legal moves in UCI format for the current chess board state."""
    return "tool_get_legal_moves result"

# TODO: tool_make_move — unknown tool class "toolmakemove"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("toolmakemove")
def tool_make_move(*args, **kwargs) -> str:
    """Executes a move on the chess board in UCI format and returns a human-readable result string."""
    return "tool_make_move result"




@CrewBase
class ConversationalChessTeam:
    """ConversationalChessTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def player_white(self) -> Agent:
        return Agent(
            config=self.agents_config['player_white'],
            tools=[tool_get_legal_moves, tool_make_move],
        )

    @agent
    def player_black(self) -> Agent:
        return Agent(
            config=self.agents_config['player_black'],
            tools=[tool_get_legal_moves, tool_make_move],
        )

    @agent
    def board_proxy(self) -> Agent:
        return Agent(
            config=self.agents_config['board_proxy'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_initiate_chat(self) -> Task:
        return Task(
            config=self.tasks_config['task_initiate_chat'],
            agent=self.player_black(),
        )

    @task
    def task_board_proxy_summary_to_white(self) -> Task:
        return Task(
            config=self.tasks_config['task_board_proxy_summary_to_white'],
            agent=self.board_proxy(),
        )

    @task
    def task_get_legal_moves(self) -> Task:
        return Task(
            config=self.tasks_config['task_get_legal_moves'],
            agent=self.player_white(),
        )

    @task
    def task_make_move(self) -> Task:
        return Task(
            config=self.tasks_config['task_make_move'],
            agent=self.player_white(),
        )

    @task
    def task_check_made_move(self) -> Task:
        return Task(
            config=self.tasks_config['task_check_made_move'],
            agent=self.board_proxy(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the ConversationalChessTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
