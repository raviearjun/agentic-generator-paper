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
        # Workflow Step: task1
        # Workflow Edge: task1 -> task2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task1")
        print("=" * 80)

        task_prompt = """Analyse in much detail the following discussion: ### DISCUSSION: {{discussion}} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: analyst, passing the
        # accumulated history so this step can see every prior step's output.
        result = await analyst.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: scriptwriter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await scriptwriter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Format the script exactly like this:   ## (person 1): (first text line from person 1)    ## (person 2): (first text line from person 2) ... """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: formatter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await formatter.run(task=history)
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