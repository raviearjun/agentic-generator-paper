import asyncio

from team import (
    financial_agent,
    research_analyst_agent,
    financial_analyst_agent,
    investment_advisor_agent,
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
        # Workflow Step: task_financial_analysis
        # Workflow Edge: task_financial_analysis -> task_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_financial_analysis")
        print("=" * 80)

        task_prompt = """Conduct a thorough analysis of {company_stock}'s stock financial health and market performance. This includes examining key financial metrics such as P/E ratio, EPS growth, revenue trends, and debt-to-equity ratio. Also, analyze the stock's performance in comparison to its industry peers and overall market trends. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: financial_analyst_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await financial_analyst_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_research
        # Workflow Edge: task_research -> task_filings_analysis
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_research")
        print("=" * 80)

        task_prompt = """Collect and summarize recent news articles, press releases, and market analyses related to the {company_stock} stock and its industry. Pay special attention to any significant events, market sentiments, and analysts' opinions. Also include upcoming events like earnings and others. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: research_analyst_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await research_analyst_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_filings_analysis
        # Workflow Edge: task_filings_analysis -> task_recommend
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_filings_analysis")
        print("=" * 80)

        task_prompt = """Analyze the latest 10-Q and 10-K filings from EDGAR for the stock {company_stock}. Focus on Management's Discussion and Analysis, financial statements, insider trading activity, and any disclosed risks. Extract relevant data and insights that could influence the stock's future performance. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: financial_analyst_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await financial_analyst_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_recommend
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_recommend")
        print("=" * 80)

        task_prompt = """Review and synthesize the analyses provided by the Financial Analyst and the Research Analyst. Combine these insights to form a comprehensive investment recommendation. Consider all aspects, including financial health, market sentiment, and qualitative data from EDGAR filings. Include insider trading activity and upcoming events like earnings. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: investment_advisor_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await investment_advisor_agent.run(task=history)
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