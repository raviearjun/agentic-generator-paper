import asyncio

from team import (
    code_writer_agent,
    code_executor_agent,
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
        # Workflow Step: task_plot_ytd_v1
        # Workflow Edge: task_plot_ytd_v1 -> task_plot_ytd_v2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_plot_ytd_v1")
        print("=" * 80)

        task_prompt = """今天是 {today}. 创建图表，显示 NVDA 和 TLSA 的股票收益。确保代码位于标记代码块中，并将图表保存到文件 ytd_stock_gains.png。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: code_executor_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await code_executor_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_plot_ytd_v2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_plot_ytd_v2")
        print("=" * 80)

        task_prompt = """Today is {today}. Download the stock prices YTD for NVDA and TSLA and create a plot. Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: code_executor_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await code_executor_agent.run(task=history)
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