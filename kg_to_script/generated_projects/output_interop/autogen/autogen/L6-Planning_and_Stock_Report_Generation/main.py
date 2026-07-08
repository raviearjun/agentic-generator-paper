import asyncio

from team import (
    admin,
    planner,
    engineer,
    executor,
    writer,
    group_chat_manager,
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
        # Workflow Step: task_initiate_write_blog
        # Workflow Edge: task_initiate_write_blog -> task_planner_plan
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_initiate_write_blog")
        print("=" * 80)

        task_prompt = """Write a blogpost about the stock price performance of Nvidia in the past month. Today's date is 2024-04-23. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: admin, passing the
        # accumulated history so this step can see every prior step's output.
        result = await admin.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_planner_plan
        # Workflow Edge: task_planner_plan -> task_engineer_write_code
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_planner_plan")
        print("=" * 80)

        task_prompt = """Given the blogpost task, determine what information can be retrieved using Python code (e.g., historical prices, volumes) and produce a stepwise plan. After each step is executed, inspect results and direct remaining steps; on failure, suggest workarounds. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: planner, passing the
        # accumulated history so this step can see every prior step's output.
        result = await planner.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_engineer_write_code
        # Workflow Edge: task_engineer_write_code -> task_executor_run_code
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_engineer_write_code")
        print("=" * 80)

        task_prompt = """Write Python code to retrieve stock data and produce analysis outputs based on the planner's specifications. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: engineer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await engineer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_executor_run_code
        # Workflow Edge: task_executor_run_code -> task_writer_produce_blog
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_executor_run_code")
        print("=" * 80)

        task_prompt = """Execute the latest code message from the engineer (look back up to last 3 messages for code), store artifacts in the 'coding' directory, and report outputs and errors. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: executor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await executor.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_writer_produce_blog
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_writer_produce_blog")
        print("=" * 80)

        task_prompt = """Write a blog post in markdown summarizing Nvidia's stock performance in the past month using provided analysis outputs. Use appropriate titles and place content in a pseudo mdcode block. Accept and apply admin feedback to refine. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: writer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await writer.run(task=history)
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