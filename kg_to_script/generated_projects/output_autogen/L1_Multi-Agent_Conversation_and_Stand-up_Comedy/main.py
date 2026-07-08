import asyncio

from team import (
    chatbot,
    unnamed,
    unnamed,
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
        # Workflow Step: task_guodegang_initiate_chat_1
        # Workflow Edge: task_guodegang_initiate_chat_1 -> task_guodegang_initiate_chat_2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_guodegang_initiate_chat_1")
        print("=" * 80)

        task_prompt = """message="我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？"; recipient=于谦; max_turns=6 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_guodegang_initiate_chat_2
        # Workflow Edge: task_guodegang_initiate_chat_2 -> task_guodegang_send_followup
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_guodegang_initiate_chat_2")
        print("=" * 80)

        task_prompt = """message="我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？"; summary_method="reflection_with_llm"; summary_prompt="简洁的总结下这场相声表演。" """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_guodegang_send_followup
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_guodegang_send_followup")
        print("=" * 80)

        task_prompt = """message='我们刚才的相声在讲什么?'; recipient=于谦 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed.run(task=history)
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