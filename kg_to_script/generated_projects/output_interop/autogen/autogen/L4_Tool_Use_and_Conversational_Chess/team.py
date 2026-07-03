"""
Auto-generated AutoGen Team: ConversationalChessTeam
Goals:
  - : Team-level goal: have the agents play a game of chess via conversational tool calls.
Capabilities:
  - : Provides legal moves for the current chess position.
  - : Apply a move to the board and update board state; produce descriptive move result.
"""

from autogen_agentchat.agents import AssistantAgent

from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_agentchat.conditions import (

    MaxMessageTermination

)

from autogen_core.tools import FunctionTool

from autogen_ext.models.openai import (
    OpenAIChatCompletionClient
)

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)


# ==================================================
# Generated Tool Stubs
# ==================================================


def tool_get_legal_moves_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_get_legal_moves

    Description:
    Returns a list of legal moves in UCI format for the current chess board state.
    """
    return (
        "Tool 'tool_get_legal_moves' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_get_legal_moves = FunctionTool(
    tool_get_legal_moves_impl,
    description="""Returns a list of legal moves in UCI format for the current chess board state. """
)


def tool_make_move_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_make_move

    Description:
    Executes a move on the chess board in UCI format and returns a human-readable result string.
    """
    return (
        "Tool 'tool_make_move' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_make_move = FunctionTool(
    tool_make_move_impl,
    description="""Executes a move on the chess board in UCI format and returns a human-readable result string. """
)


# ==================================================
# Agents
# ==================================================


player_white = AssistantAgent(
    name="player_white",
    model_client=model_client,
    system_message="""
Role:
Chess Player (White)

Goal:
Chess Player (White)

Background:
You are a Chess Player (White).
""",
)


player_black = AssistantAgent(
    name="player_black",
    model_client=model_client,
    system_message="""
Role:
Chess Player (Black)

Goal:
Chess Player (Black)

Background:
You are a Chess Player (Black).
""",
)


board_proxy = AssistantAgent(
    name="board_proxy",
    model_client=model_client,
    system_message="""
Role:
Board Proxy / Referee

Goal:
Board Proxy / Referee

Background:
You are a Board Proxy / Referee.
""",
)



