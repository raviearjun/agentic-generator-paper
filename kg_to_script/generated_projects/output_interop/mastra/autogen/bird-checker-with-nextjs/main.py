import asyncio

from team import (
    bird_agent,
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
        # Workflow Step: get_image_task
        # Workflow Edge: get_image_task -> bird_check_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: get_image_task")
        print("=" * 80)

        task_prompt = """Fetch a random image from Unsplash matching the provided query (wildlife | feathers | flying | birds). """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: bird_check_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: bird_check_task")
        print("=" * 80)

        task_prompt = """view this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: bird_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await bird_agent.run(task=history)
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