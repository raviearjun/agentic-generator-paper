import asyncio

from team import (
    spamfilter,
    analyst,
    scriptwriter,
    formatter,
    scorer,
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
        # Workflow Step: task1
        # Workflow Edge: task1 -> task2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task1")
        print("=" * 80)

        task_prompt = """Analyse in much detail the following discussion: ### DISCUSSION: {{discussion}} """
        # Execute via the assigned agent: analyst
        result = await analyst.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task2
        # Workflow Edge: task2 -> task3
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task2")
        print("=" * 80)

        task_prompt = """Create a dialogue heavy screenplay from the discussion, between two persons. Do NOT write parentheticals. Leave out wrylies. You MUST SKIP directional notes. """
        # Execute via the assigned agent: scriptwriter
        result = await scriptwriter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task3
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task3")
        print("=" * 80)

        task_prompt = """Format the script exactly like this:   ## (person 1): (first text line from person 1) ... """
        # Execute via the assigned agent: formatter
        result = await formatter.run(task=task_prompt)

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