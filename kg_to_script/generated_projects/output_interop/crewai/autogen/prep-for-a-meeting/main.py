import asyncio

from team import (
    researcher_agent,
    industry_analyst_agent,
    meeting_strategy_agent,
    summary_and_briefing_agent,
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
        # Workflow Step: research_task
        # Workflow Edge: research_task -> industry_analysis_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: research_task")
        print("=" * 80)

        task_prompt = """Conduct comprehensive research on each of the individuals and companies
involved in the upcoming meeting. Gather information on recent
news, achievements, professional background, and any relevant
business activities.

Participants: {participants}
Meeting Context: {context} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: researcher_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await researcher_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: industry_analysis_task
        # Workflow Edge: industry_analysis_task -> meeting_strategy_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: industry_analysis_task")
        print("=" * 80)

        task_prompt = """Analyze the current industry trends, challenges, and opportunities
relevant to the meeting's context. Consider market reports, recent
developments, and expert opinions to provide a comprehensive
overview of the industry landscape.

Participants: {participants}
Meeting Context: {context} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: industry_analyst_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await industry_analyst_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: meeting_strategy_task
        # Workflow Edge: meeting_strategy_task -> summary_and_briefing_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: meeting_strategy_task")
        print("=" * 80)

        task_prompt = """Develop strategic talking points, questions, and discussion angles
for the meeting based on the research and industry analysis conducted

Meeting Context: {context}
Meeting Objective: {objective} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: meeting_strategy_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await meeting_strategy_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: summary_and_briefing_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: summary_and_briefing_task")
        print("=" * 80)

        task_prompt = """Compile all the research findings, industry analysis, and strategic
talking points into a concise, comprehensive briefing document for
the meeting.
Ensure the briefing is easy to digest and equips the meeting
participants with all necessary information and strategies.

Meeting Context: {context}
Meeting Objective: {objective} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: summary_and_briefing_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await summary_and_briefing_agent.run(task=history)
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