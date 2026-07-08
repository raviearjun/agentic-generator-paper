import asyncio

from team import (
    trade_agent,
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
        # Workflow Step: open_buy_ui_task
        # Workflow Edge: open_buy_ui_task -> execute_purchase_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: open_buy_ui_task")
        print("=" * 80)

        task_prompt = """Open the buy stock user interface for the specified ticker and prefill price information. Expected output: UI displayed and ready for user input. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trade_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trade_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: execute_purchase_task
        # Workflow Edge: execute_purchase_task -> confirm_purchase_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: execute_purchase_task")
        print("=" * 80)

        task_prompt = """Invoke the 'buy-stock' tool with JSON: { purchaseDetails: { ticker: <string>, quantity: <integer>, price: <number> } }. Expect the tool to return a confirmation payload. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trade_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trade_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: confirm_purchase_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: confirm_purchase_task")
        print("=" * 80)

        task_prompt = """Present the purchase confirmation message to the user, showing ticker, quantity, price, and total cost. Expected output: confirmation message shown in UI. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trade_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trade_agent.run(task=history)
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