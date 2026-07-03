"""
Auto-generated CrewAI Crew: OnboardingTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Gather customer's name and location.
  - : Collect customer's preferences on news topics.
  - : Provide engaging and fun content based on customer's info and topic preferences.
Human Agents:
  - agent_customer_proxy_agent (customer_proxy)
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class OnboardingTeam:
    """OnboardingTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def onboarding_personal_information_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['onboarding_personal_information_agent'],
        )

    @agent
    def onboarding_topic_preference_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['onboarding_topic_preference_agent'],
        )

    @agent
    def customer_engagement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['customer_engagement_agent'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_onboarding_personal_info(self) -> Task:
        return Task(
            config=self.tasks_config['task_onboarding_personal_info'],
            agent=self.onboarding_personal_information_agent(),
        )

    @task
    def task_onboarding_topic_preference(self) -> Task:
        return Task(
            config=self.tasks_config['task_onboarding_topic_preference'],
            agent=self.onboarding_topic_preference_agent(),
        )

    @task
    def task_customer_engagement_request(self) -> Task:
        return Task(
            config=self.tasks_config['task_customer_engagement_request'],
            agent=self.customer_engagement_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the OnboardingTeam"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
