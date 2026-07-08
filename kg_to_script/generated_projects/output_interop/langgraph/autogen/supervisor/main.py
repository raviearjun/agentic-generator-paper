import asyncio

from team import (
    supervisor,
    router,
    general_input,
    stockbroker,
    trip_planner,
    open_code,
    order_pizza,
    writer_agent,
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
        # Workflow Step: task_start
        # Workflow Edge: task_start -> task_router
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_start")
        print("=" * 80)

        task_prompt = """Start step for the supervisor StateGraph that initializes routing to the 'router' step. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: supervisor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await supervisor.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_router
        # Workflow Edge: task_router -> task_stockbroker
        # Workflow Edge: task_router -> task_trip_planner
        # Workflow Edge: task_router -> task_open_code
        # Workflow Edge: task_router -> task_order_pizza
        # Workflow Edge: task_router -> task_general_input
        # Workflow Edge: task_router -> task_writer_agent
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_router")
        print("=" * 80)

        task_prompt = """The route to take based on the user's input.
- stockbroker: can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio
- tripPlanner: helps the user plan their trip. it can suggest restaurants, and places to stay in any given location.
- openCode: can write a React TODO app for the user. Only call this tool if they request a TODO app.
- orderPizza: can order a pizza for the user
- writerAgent: can write a text document for the user. Only call this tool if they request a text document.
- generalInput: handles all other cases where the above tools don't apply

You're a highly helpful AI assistant, tasked with routing the user's query to the appropriate tool.
You should analyze the user's input, and choose the appropriate tool to use.

The expected output is a single route name: one of {stockbroker, tripPlanner, openCode, orderPizza, generalInput, writerAgent}. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: router, passing the
        # accumulated history so this step can see every prior step's output.
        result = await router.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_stockbroker
        # Workflow Edge: task_stockbroker -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_stockbroker")
        print("=" * 80)

        task_prompt = """Tool: stockbroker — can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: stockbroker, passing the
        # accumulated history so this step can see every prior step's output.
        result = await stockbroker.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_trip_planner
        # Workflow Edge: task_trip_planner -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_trip_planner")
        print("=" * 80)

        task_prompt = """Tool: tripPlanner — helps the user plan their trip; can suggest restaurants and places to stay for a given location. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trip_planner, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trip_planner.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_open_code
        # Workflow Edge: task_open_code -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_open_code")
        print("=" * 80)

        task_prompt = """Tool: openCode — can write a React TODO app for the user. Only call this tool if they request a TODO app. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: open_code, passing the
        # accumulated history so this step can see every prior step's output.
        result = await open_code.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_order_pizza
        # Workflow Edge: task_order_pizza -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_order_pizza")
        print("=" * 80)

        task_prompt = """Tool: orderPizza — can order a pizza for the user. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: order_pizza, passing the
        # accumulated history so this step can see every prior step's output.
        result = await order_pizza.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_general_input
        # Workflow Edge: task_general_input -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_general_input")
        print("=" * 80)

        task_prompt = """You are an AI assistant.
If the user asks what you can do, describe these tools.
- stockbroker: can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio
- tripPlanner: helps the user plan their trip. it can suggest restaurants, and places to stay in any given location.
- openCode: can write a React TODO app for the user. Only call this tool if they request a TODO app.
- orderPizza: can order a pizza for the user
- writerAgent: can write a text document for the user. Only call this tool if they request a text document.

If the last message is a tool result, describe what the action was, congratulate the user, or send a friendly followup in response to the tool action. Ensure this is a clear and concise message.

Otherwise, just answer as normal. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: general_input, passing the
        # accumulated history so this step can see every prior step's output.
        result = await general_input.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_writer_agent
        # Workflow Edge: task_writer_agent -> task_end
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_writer_agent")
        print("=" * 80)

        task_prompt = """Tool: writerAgent — can write a text document for the user. Only call this tool if they request a text document. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: writer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await writer_agent.run(task=history)
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

        task_prompt = """End step for the supervisor StateGraph indicating the workflow is complete. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: supervisor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await supervisor.run(task=history)
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