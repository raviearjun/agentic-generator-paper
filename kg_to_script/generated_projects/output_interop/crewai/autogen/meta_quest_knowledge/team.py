"""
Auto-generated AutoGen Team: MetaQuestKnowledgeCrew
Goals:
  - : Agent-level goal extracted from agents.yaml.
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


# ==================================================
# Agents
# ==================================================


meta_quest_expert = AssistantAgent(
    name="meta_quest_expert",
    model_client=model_client,
    system_message="""
Role:
Meta Quest Expert

Goal:
Agent-level goal extracted from agents.yaml.

Background:
You are a Meta Quest Expert.
""",
)



