import asyncio

from team import (
    agent_1_name,
    agent_2_name,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution
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
        # Execute via the assigned agent: agent_1_name
        result = await agent_1_name.run(task=task_prompt)

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
        # Execute via the assigned agent: agent_2_name
        result = await agent_2_name.run(task=task_prompt)

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