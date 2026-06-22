"""
Auto-generated CrewAI Crew: JobPostingCrewTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - Hiring Goal: Goal: hire for the specified hiring needs (e.g., Production Assistant for TV production in Los Angeles, June 2025) using a compelling job posting aligned with company values.
Objectives:
  - Create Job Posting Objective: Collective objective: produce a job posting that aligns with company culture and hiring needs.
Resources:
  - DefaultInputs for JobPostingCrew: Example input values used for kickoff/train:
- company_domain: careers.wbd.com
- company_description: Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world’s most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We're home to the world’s best storytellers, creating world-class products for consumers
- hiring_needs: Production Assistant, for a TV production set in Los Angeles in June 2025
- specific_benefits: Weekly Pay, Employee Meals, healthcare
These are preserved as the default input bundle used to initiate the crew."
  - job_description_example.md: # Amazing Job Description Example

## Company Overview
At InnovateTech, we're at the forefront of digital transformation, leveraging cutting-edge technologies to create impactful solutions. Our culture thrives on innovation, collaboration, and a commitment to excellence. Join us to be a part of a dynamic team shaping the future of tech.

## Job Title: Senior Software Engineer

### Location
Remote - Global Team

### Job Summary
As a Senior Software Engineer at InnovateTech, you'll lead the development of scalable software solutions that revolutionize how businesses interact with technology. You'll collaborate with cross-functional teams to drive projects from conception to deployment, ensuring high-quality and innovative outcomes.

### Responsibilities
- Design, develop, and implement high-quality software solutions that align with our strategic direction.
- Lead technical discussions and decision-making processes to drive technology forward.
- Mentor junior engineers, providing guidance and support to foster a culture of excellence and growth.
- Collaborate with stakeholders across the company to understand requirements and deliver beyond expectations.
- Stay abreast of industry trends and emerging technologies to incorporate best practices into our workflows.

### Requirements
- Bachelor's degree in Computer Science, Engineering, or related field.
- 5+ years of experience in software development, with a strong background in [Specific Technology/Programming Language].
- Proven track record of leading successful projects from inception to completion.
- Excellent problem-solving skills and a passion for technology.
- Strong communication and teamwork abilities.

### Benefits
- Competitive salary and equity package.
- Comprehensive health, dental, and vision insurance.
- Unlimited PTO to promote work-life balance.
- Remote work flexibility.
- Professional development stipends.
- Monthly wellness allowances.
- Inclusive and dynamic work culture.

### How to Apply
Please submit your resume, cover letter, and any relevant portfolio links to careers@innovatetech.com with the subject "Senior Software Engineer Application". We're excited to hear from you!

---

InnovateTech is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees.
  - draft_job_posting.md: Draft job posting produced by DraftJobPostingTask; initial markdown draft.
  - final_job_posting.md: Review-edited, final job posting in markdown, ready for publishing.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import WebsiteSearchTool, SerperDevTool, FileReadTool

# ===========================================================
# Tool Instances
# ===========================================================
website_search_tool = WebsiteSearchTool()
serper_dev_tool = SerperDevTool()
file_read_tool = FileReadTool(file_path="job_description_example.md", description="A tool to read the job description example file.")



@CrewBase
class JobPostingCrewTeam:
    """JobPostingCrewTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'],
            tools=[website_search_tool, serper_dev_tool],
        )

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            tools=[website_search_tool, serper_dev_tool, file_read_tool],
        )

    @agent
    def review_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['review_agent'],
            tools=[website_search_tool, serper_dev_tool, file_read_tool],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def research_company_culture_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_company_culture_task'],
            agent=self.research_agent(),
        )

    @task
    def research_role_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_role_requirements_task'],
            agent=self.research_agent(),
        )

    @task
    def draft_job_posting_task(self) -> Task:
        return Task(
            config=self.tasks_config['draft_job_posting_task'],
            agent=self.writer_agent(),
            context=[self.research_company_culture_task()],
        )

    @task
    def review_and_edit_job_posting_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_and_edit_job_posting_task'],
            agent=self.review_agent(),
            context=[self.draft_job_posting_task()],
        )

    @task
    def industry_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['industry_analysis_task'],
            agent=self.research_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the JobPostingCrewTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
