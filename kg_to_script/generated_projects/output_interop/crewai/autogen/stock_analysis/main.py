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

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution
        # ==================================================
        # Workflow Step: task_financial_analysis
        # Workflow Edge: task_financial_analysis -> task_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_financial_analysis")
        print("=" * 80)

        task_prompt = """Conduct a thorough analysis of {company_stock}'s stock financial health and market performance. """
        # Execute via the assigned agent: financial_analyst_agent
        result = await financial_analyst_agent.run(task=task_prompt)

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

        task_prompt = """Collect and summarize recent news articles, press releases, and market analyses related to the {company_stock} stock and its industry. """
        # Execute via the assigned agent: research_analyst_agent
        result = await research_analyst_agent.run(task=task_prompt)

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

        task_prompt = """Analyze the latest 10-Q and 10-K filings from EDGAR for the stock {company_stock} in question. """
        # Execute via the assigned agent: financial_analyst_agent
        result = await financial_analyst_agent.run(task=task_prompt)

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

        task_prompt = """Review and synthesize the analyses provided by the Financial Analyst and the Research Analyst to form a comprehensive investment recommendation. """
        # Execute via the assigned agent: investment_advisor_agent
        result = await investment_advisor_agent.run(task=task_prompt)

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