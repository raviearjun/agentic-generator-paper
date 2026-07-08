import asyncio

from team import (
    senior_engineer_agent,
    qa_engineer_agent,
    chief_qa_engineer_agent,
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
        # Workflow Step: task_code
        # Workflow Edge: task_code -> task_review
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_code")
        print("=" * 80)

        task_prompt = """You will create a game using python, these are the instructions:

Instructions
# ------------
{game} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_engineer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_engineer_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_review
        # Workflow Edge: task_review -> task_evaluate
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_review")
        print("=" * 80)

        task_prompt = """You will create a game using python, these are the instructions:

Instructions
# ------------
{game}

Using the code you got, check for errors. Check for logic errors,
syntax errors, missing imports, variable declarations, mismatched brackets,
and security vulnerabilities. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: qa_engineer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await qa_engineer_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_evaluate
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_evaluate")
        print("=" * 80)

        task_prompt = """You are helping create a game using python, these are the instructions:

Instructions
# ------------
{game}

You will look over the code to insure that it is complete and
does the job that it is supposed to do. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chief_qa_engineer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chief_qa_engineer_agent.run(task=history)
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