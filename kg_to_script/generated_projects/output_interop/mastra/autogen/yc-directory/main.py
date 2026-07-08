import asyncio

from team import (
    yc_directory_agent,
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
        # Workflow Step: fetch_yc_directory_task
        # Workflow Edge: fetch_yc_directory_task -> process_yc_data_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: fetch_yc_directory_task")
        print("=" * 80)

        task_prompt = """Invoke the 'yc-directory' tool to retrieve the full 2024 YC directory. Return the array of company objects exactly as provided by the tool. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: yc_directory_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await yc_directory_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: process_yc_data_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: process_yc_data_task")
        print("=" * 80)

        task_prompt = """Format the retrieved YC directory data for user-friendly responses. Ensure each company mentions its batch and includes name, industries, and short summary. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: yc_directory_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await yc_directory_agent.run(task=history)
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