import asyncio

from team import (
    research_agent,
    writer_agent,
    review_agent,
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
        # Workflow Step: research_company_culture_task
        # Workflow Edge: research_company_culture_task -> research_role_requirements_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: research_company_culture_task")
        print("=" * 80)

        task_prompt = """Analyze the provided company website and the hiring manager's company's domain {company_domain}, description {company_description}. Focus on understanding the company's culture, values, and mission. Identify unique selling points and specific projects or achievements highlighted on the site. Compile a report summarizing these insights, specifically how they can be leveraged in a job posting to attract the right candidates. """
        # Execute via the assigned agent: research_agent
        result = await research_agent.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: research_role_requirements_task
        # Workflow Edge: research_role_requirements_task -> draft_job_posting_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: research_role_requirements_task")
        print("=" * 80)

        task_prompt = """Based on the hiring manager's needs: {hiring_needs}, identify the key skills, experiences, and qualities the ideal candidate should possess for the role. Consider the company's current projects, its competitive landscape, and industry trends. Prepare a list of recommended job requirements and qualifications that align with the company's needs and values. """
        # Execute via the assigned agent: research_agent
        result = await research_agent.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: draft_job_posting_task
        # Workflow Edge: draft_job_posting_task -> review_and_edit_job_posting_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: draft_job_posting_task")
        print("=" * 80)

        task_prompt = """Draft a job posting for the role described by the hiring manager: {hiring_needs}. Use the insights on {company_description} to start with a compelling introduction, followed by a detailed role description, responsibilities, and required skills and qualifications. Ensure the tone aligns with the company's culture and incorporate any unique benefits or opportunities offered by the company. Specific benefits: {specific_benefits}. """
        # Execute via the assigned agent: writer_agent
        result = await writer_agent.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: review_and_edit_job_posting_task
        # Workflow Edge: review_and_edit_job_posting_task -> industry_analysis_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: review_and_edit_job_posting_task")
        print("=" * 80)

        task_prompt = """Review the draft job posting for the role {hiring_needs}. Check for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values. Edit and refine the content, ensuring it speaks directly to the desired candidates and accurately reflects the role's unique benefits and opportunities. Provide feedback for any necessary revisions. """
        # Execute via the assigned agent: review_agent
        result = await review_agent.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: industry_analysis_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: industry_analysis_task")
        print("=" * 80)

        task_prompt = """Conduct an in-depth analysis of the industry related to the company's domain {company_domain}. Investigate current trends, challenges, and opportunities within the industry, utilizing market reports, recent developments, and expert opinions. Assess how these factors could impact the role being hired for and the overall attractiveness of the position to potential candidates. """
        # Execute via the assigned agent: research_agent
        result = await research_agent.run(task=task_prompt)

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