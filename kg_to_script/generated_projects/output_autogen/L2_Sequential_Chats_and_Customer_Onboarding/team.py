"""
Auto-generated AutoGen Team: OnboardingTeam
Goals:
  - : Gather customer's name and location.
  - : Collect customer's preferences on news topics.
  - : Provide engaging and fun content based on customer's info and topic preferences.
Human Agents:
  - agent_customer_proxy_agent (customer_proxy)
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import UserProxyAgent

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


onboarding_personal_information_agent = AssistantAgent(
    name="onboarding_personal_information_agent",
    model_client=model_client,
    system_message="""
Role:
onboarding_personal_information

Goal:
Gather customer's name and location.

Background:
You are a onboarding_personal_information.
""",
)


onboarding_topic_preference_agent = AssistantAgent(
    name="onboarding_topic_preference_agent",
    model_client=model_client,
    system_message="""
Role:
onboarding_topic_preference

Goal:
Collect customer's preferences on news topics.

Background:
You are a onboarding_topic_preference.
""",
)


customer_engagement_agent = AssistantAgent(
    name="customer_engagement_agent",
    model_client=model_client,
    system_message="""
Role:
customer_engagement

Goal:
Provide engaging and fun content based on customer's info and topic preferences.

Background:
You are a customer_engagement.
""",
)


# ==================================================
# Human Agents (UserProxy)
# ==================================================

agent_customer_proxy_agent = UserProxyAgent(
    name="agent_customer_proxy_agent",
    description="""customer_proxy """,
)

