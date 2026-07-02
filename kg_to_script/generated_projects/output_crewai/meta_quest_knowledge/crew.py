"""
Auto-generated CrewAI Crew: MetaQuestKnowledgeCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Agent-level goal extracted from agents.yaml.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class MetaQuestKnowledgeCrew:
    """MetaQuestKnowledgeCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def meta_quest_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['meta_quest_expert'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def answer_question_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_question_task'],
            agent=self.meta_quest_expert(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the MetaQuestKnowledgeCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
