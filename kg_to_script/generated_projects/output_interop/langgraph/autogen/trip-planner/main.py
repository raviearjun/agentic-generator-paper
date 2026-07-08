import asyncio

from team import (
    trip_planner_agent,
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
        # Workflow Step: view_accommodations_task
        # Workflow Edge: view_accommodations_task -> select_accommodation_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: view_accommodations_task")
        print("=" * 80)

        task_prompt = """List available accommodations with images, ratings, price, and brief details. Allow the user to open details of an accommodation. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trip_planner_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trip_planner_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: select_accommodation_task
        # Workflow Edge: select_accommodation_task -> confirm_booking_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: select_accommodation_task")
        print("=" * 80)

        task_prompt = """When a user selects an accommodation, present full details (name, rating, price, dates, guests) and provide a booking action trigger. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trip_planner_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trip_planner_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: confirm_booking_task
        # Workflow Edge: confirm_booking_task -> booked_confirmation_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: confirm_booking_task")
        print("=" * 80)

        task_prompt = """Construct a JSON payload with fields { accommodation, tripDetails } and call the 'book-accommodation' tool. After tool invocation, provide a human-facing confirmation message describing the booked accommodation and trip summary. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trip_planner_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trip_planner_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: booked_confirmation_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: booked_confirmation_task")
        print("=" * 80)

        task_prompt = """Show booked accommodation summary including dates, guest count, address/name, rating and total price. If tool response includes booking reference, display it. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: trip_planner_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await trip_planner_agent.run(task=history)
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