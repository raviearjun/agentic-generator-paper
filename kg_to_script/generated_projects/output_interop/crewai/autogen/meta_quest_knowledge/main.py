import asyncio

from team import (
    meta_quest_expert,
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
        # Workflow Step: answer_question_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: answer_question_task")
        print("=" * 80)

        task_prompt = """Answer the user question with the most relevant information from the context and available knowledge sources.
Question: {question}

Do not answer questions that are not related to the context or knowledge sources. """
        # Execute via the assigned agent: meta_quest_expert
        result = await meta_quest_expert.run(task=task_prompt)

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