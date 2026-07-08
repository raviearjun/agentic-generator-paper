import asyncio

from team import (
    stock_agent,
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
        # Workflow Step: task_init
        # Workflow Edge: task_init -> task_query
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_init")
        print("=" * 80)

        task_prompt = """Initialize the Stock Agent before handling requests. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: stock_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await stock_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_query
        # Workflow Edge: task_query -> task_tool_call
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_query")
        print("=" * 80)

        task_prompt = """What is the current stock price of Apple (AAPL)? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: stock_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await stock_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_tool_call
        # Workflow Edge: task_tool_call -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_tool_call")
        print("=" * 80)

        task_prompt = """Call the stockPrices tool with symbol 'AAPL' to fetch the latest closing price. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: stock_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await stock_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_end")
        print("=" * 80)

        task_prompt = """Return the formatted current price to the user. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: stock_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await stock_agent.run(task=history)
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