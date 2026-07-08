import asyncio

from team import (
    agent_1_name,
    agent_2_name,
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
        # Workflow Step: task_1
        # Workflow Edge: task_1 -> task_2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_1")
        print("=" * 80)

        task_prompt = """Do something as part of task 1

If you do your BEST WORK, I'll give you a $10,000 commission!

Make sure to use the most recent data as possible.

Use this variable: {var1}
And also this variable: {var2} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_1_name, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_1_name.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_2")
        print("=" * 80)

        task_prompt = """Take the input from task 1 and do something with it.

If you do your BEST WORK, I'll give you a $10,000 commission!

Make sure to do something else. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_2_name, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_2_name.run(task=history)
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