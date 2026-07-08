import asyncio

from team import (
    langgraph_anthropic_agent,
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
        # Workflow Step: find_store_task
        # Workflow Edge: find_store_task -> order_pizza_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: find_store_task")
        print("=" * 80)

        task_prompt = """You are a helpful AI assistant, tasked with extracting information from the conversation between you, and the user, in order to find a pizza shop for them. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: langgraph_anthropic_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await langgraph_anthropic_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: order_pizza_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: order_pizza_task")
        print("=" * 80)

        task_prompt = """You are a helpful AI assistant, tasked with placing an order for a pizza for the user. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: langgraph_anthropic_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await langgraph_anthropic_agent.run(task=history)
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