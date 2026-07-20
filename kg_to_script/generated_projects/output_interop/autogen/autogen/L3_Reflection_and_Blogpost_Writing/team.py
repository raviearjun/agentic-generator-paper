
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


unnamed_writer = AssistantAgent(
    name="writer",
    model_client=model_client,
    system_message="""
Role:
Writer

Goal:
Writer

Background:
You are a Writer.
""",
)


unnamed_critic = AssistantAgent(
    name="critic",
    model_client=model_client,
    system_message="""
Role:
Critic

Goal:
Critic

Background:
You are a Critic.
""",
)


unnamed_seo = AssistantAgent(
    name="seo_reviewer",
    model_client=model_client,
    system_message="""
Role:
SEO Reviewer

Goal:
SEO Reviewer

Background:
You are a SEO Reviewer.
""",
)


unnamed_legal = AssistantAgent(
    name="legal_reviewer",
    model_client=model_client,
    system_message="""
Role:
Legal Reviewer

Goal:
Legal Reviewer

Background:
You are a Legal Reviewer.
""",
)


unnamed_ethics = AssistantAgent(
    name="ethics_reviewer",
    model_client=model_client,
    system_message="""
Role:
Ethics Reviewer

Goal:
Ethics Reviewer

Background:
You are a Ethics Reviewer.
""",
)


unnamed_meta = AssistantAgent(
    name="meta_reviewer",
    model_client=model_client,
    system_message="""
Role:
Meta Reviewer

Goal:
Meta Reviewer

Background:
You are a Meta Reviewer.
""",
)



