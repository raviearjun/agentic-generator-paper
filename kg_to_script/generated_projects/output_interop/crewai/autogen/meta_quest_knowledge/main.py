import asyncio

from team import (
    meta_quest_expert,
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
        # Workflow Step: answer_question_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: answer_question_task")
        print("=" * 80)

        task_prompt = """Answer the user question with the most relevant information from the context and available knowledge sources.
Question: {question}

Do not answer questions that are not related to the context or knowledge sources. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: meta_quest_expert, passing the
        # accumulated history so this step can see every prior step's output.
        result = await meta_quest_expert.run(task=history)
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