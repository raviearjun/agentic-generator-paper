import asyncio

from team import (
    mastra_llm,
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
        # Workflow Step: gather_candidate_info_task
        # Workflow Edge: gather_candidate_info_task -> ask_about_specialty_task
        # Workflow Edge: gather_candidate_info_task -> ask_about_role_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: gather_candidate_info_task")
        print("=" * 80)

        task_prompt = """You are given this resume text: "${resumeText}" """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: mastra_llm, passing the
        # accumulated history so this step can see every prior step's output.
        result = await mastra_llm.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: ask_about_specialty_task
        # Workflow Edge: ask_about_specialty_task -> ask_about_role_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: ask_about_specialty_task")
        print("=" * 80)

        task_prompt = """You are a recruiter. Given the resume below, craft a short question for ${candidateName} about how they got into "${specialty}". Resume: ${resumeText} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: mastra_llm, passing the
        # accumulated history so this step can see every prior step's output.
        result = await mastra_llm.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: ask_about_role_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: ask_about_role_task")
        print("=" * 80)

        task_prompt = """You are a recruiter. Given the resume below, craft a short question for ${candidateName} asking what interests them most about this role. Resume: ${resumeText} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: mastra_llm, passing the
        # accumulated history so this step can see every prior step's output.
        result = await mastra_llm.run(task=history)
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