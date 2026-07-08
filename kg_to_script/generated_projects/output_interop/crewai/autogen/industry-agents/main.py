import asyncio

from team import (
    biomedical_marketing_agent,
    healthcare_marketing_agent,
    financial_marketing_agent,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)
from autogen_agentchat.messages import BaseChatMessage, TextMessage

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution.
        #
        # `history` accumulates every step's real conversation so far and is
        # threaded into each subsequent step's .run() call. Without this,
        # each step only ever sees its own task prompt in isolation - later
        # steps (e.g. "review the draft") have no way to see what an earlier
        # step (e.g. "draft the posting") actually produced.
        history: list[BaseChatMessage] = []
        # ==================================================
        # Workflow Step: task_biomedical_research
        # Workflow Edge: task_biomedical_research -> task_healthcare_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_biomedical_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about {weaviate_feature}
Make sure you find any interesting and relevant information using the web and Weaviate blogs. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: biomedical_marketing_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await biomedical_marketing_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_healthcare_research
        # Workflow Edge: task_healthcare_research -> task_financial_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_healthcare_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about {weaviate_feature}
Make sure you find any interesting and relevant information using the web and Weaviate blogs. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: healthcare_marketing_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await healthcare_marketing_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_financial_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_financial_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about {weaviate_feature}
Make sure you find any interesting and relevant information using the web and Weaviate blogs. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: financial_marketing_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await financial_marketing_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        print("\n" + "=" * 80)
        print("DONE")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)
        print(type(e).__name__)
        print(str(e))



if __name__ == "__main__":
    asyncio.run(main())