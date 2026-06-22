"""
Auto-generated CrewAI Crew: RecruitmentCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - Find potential candidates for the job: Find potential candidates for the job specified in inputs (job_requirements). Use multiple public resources to assemble candidate brief profiles and contact info.
  - Match the candidates to the best jobs and score them: Evaluate candidates relative to the job_requirements, compute scores and rank candidates with justifications.
  - Develop outreach strategies for the selected candidates: Produce outreach methods and message templates tailored to prioritized candidates.
  - Report the best candidates to the recruiters: Assemble a concise report for recruiters with profiles, scores, and outreach plan; follow output formatting instruction from tasks configuration.
Objectives:
  - Find and report best candidates for a job opening: Coordinate research, matching/scoring, outreach strategy, and reporting to produce a ranked and actionable list of candidates for a given job requirement input.
Capabilities:
  - candidate_research: Search public data sources and extract candidate basic profile information.
  - candidate_matching_and_scoring: Evaluate candidates against job requirements and produce a numeric or ordinal score and justification.
  - outreach_strategy_development: Design outreach approaches and generate template messages for contacting candidates.
  - candidate_reporting: Compose recruiter-facing reports summarizing findings, scores and outreach strategies.
  - search_api: 
  - web_scraping: 
  - retrieve_linkedin_profiles: 
Resources:
  - candidates_raw_list: Raw list of found candidate profiles and their basic contact/profile information produced by research_candidates_task.
  - candidates_scored: Candidates evaluated and scored by match_and_score_candidates_task; contains scores and justifications.
  - outreach_plan: Outreach methods and message templates produced by outreach_strategy_task.
  - final_report_for_recruiters: Compiled report produced by report_candidates_task with recommended candidates, scores, and outreach templates.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# ===========================================================
# Tool Instances
# ===========================================================
tool_serperdev = SerperDevTool(name="SerperDevTool", name="Search API tool, configuration may include API key and search parameters (not included here).", note="SerperDevTool", note="Search API tool, configuration may include API key and search parameters (not included here).")
tool_scrapewebsite = ScrapeWebsiteTool(name="ScrapeWebsiteTool", name="Generic HTML scraping tool used to extract elements by CSS selectors.", note="ScrapeWebsiteTool", note="Generic HTML scraping tool used to extract elements by CSS selectors.")
# TODO: tool_linkedin — unknown tool class "RetrieveLinkedInprofiles"
#   Description: Retrieve LinkedIn profiles given a list of skills. Input is a comma-separated li
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# tool_linkedin = SomeCustomTool(name="LinkedInTool", name="This tool requires a LinkedIn session cookie available via environment variable LINKEDIN_COOKIE. The client will navigate linkedin.com and extract profiles.", note="LinkedInTool", note="This tool requires a LinkedIn session cookie available via environment variable LINKEDIN_COOKIE. The client will navigate linkedin.com and extract profiles.")



@CrewBase
class RecruitmentCrew:
    """RecruitmentCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[tool_serperdev, tool_scrapewebsite, tool_linkedin],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[tool_serperdev, tool_scrapewebsite],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def communicator(self) -> Agent:
        return Agent(
            config=self.agents_config['communicator'],
            tools=[tool_serperdev, tool_scrapewebsite],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            allow_delegation=False,
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def research_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_candidates_task'],
            agent=self.researcher(),
        )

    @task
    def match_and_score_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_and_score_candidates_task'],
            agent=self.matcher(),
        )

    @task
    def outreach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['outreach_strategy_task'],
            agent=self.communicator(),
        )

    @task
    def report_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_candidates_task'],
            agent=self.reporter(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the RecruitmentCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
