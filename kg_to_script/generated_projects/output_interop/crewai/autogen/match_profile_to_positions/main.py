import asyncio

from team import (
    cv_reader,
    matcher,
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
        # Workflow Step: task_read_cv
        # Workflow Edge: task_read_cv -> task_match_cv
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_read_cv")
        print("=" * 80)

        task_prompt = """Extract relevant information from the given CV. Focus on skills, experience, education, and key achievements.
Ensure to capture the candidate's professional summary, technical skills, work history, and educational background.

CV file: {path_to_cv} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cv_reader, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cv_reader.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_match_cv
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_match_cv")
        print("=" * 80)

        task_prompt = """Match the CV to the job opportunities based on skills, experience, and key achievements.
Evaluate how well the candidate's profile fits each job description, focusing on the alignment of skills, work history, and key achievements with the job requirements.

Jobs CSV file: {path_to_jobs_csv}

CV file: {path_to_cv} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: matcher, passing the
        # accumulated history so this step can see every prior step's output.
        result = await matcher.run(task=history)
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