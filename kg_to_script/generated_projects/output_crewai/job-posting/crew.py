"""
Auto-generated CrewAI Crew: JobPostingCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Analyze the company website and provided description to extract insights on culture, values, and specific needs.
  - : Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.
  - : Review the job posting for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values.
  - : Automate the creation of job postings using CrewAI to analyze company information and produce polished job descriptions and analyses.
Capabilities:
  - : Performs general website search and retrieval.
  - : Uses Serper.dev API for search and rich web results.
  - : Reads the contents of a local file for use by agents.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import WebsiteSearchTool, SerperDevTool, FileReadTool

# ===========================================================
# Tool Instances
# ===========================================================
website_search_tool = WebsiteSearchTool(api_key="unspecified")
serper_dev_tool = SerperDevTool(api_key="unspecified")
file_read_tool = FileReadTool(file_path="job_description_example.md")



@CrewBase
class JobPostingCrew:
    """JobPostingCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'],
            tools=[website_search_tool, serper_dev_tool],
            verbose=True,
        )

    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            tools=[website_search_tool, serper_dev_tool, file_read_tool],
            verbose=True,
        )

    @agent
    def review_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['review_agent'],
            tools=[website_search_tool, serper_dev_tool, file_read_tool],
            verbose=True,
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
        )

    @task
    def review_and_edit_job_posting_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_and_edit_job_posting_task'],
            agent=self.review_agent(),
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
        """Creates the JobPostingCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
