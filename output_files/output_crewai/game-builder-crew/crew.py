"""
Auto-generated CrewAI Crew: GameBuilderCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - Create Game (Team Goal): Produce a working python game implementation given a textual game description input. The system assembles agents and tasks to generate, review, and evaluate final python code for a game (examples include Pac-Man and Snake).
  - Create software as needed: Create software as needed
  - Create Perfect code: Create Perfect code, by analyzing the code that is given for errors
  - Ensure the code does the job that it is supposed to do: Ensure that the code fulfills the functional requirements of the game description and is complete.
Resources:
  - initial_game_code: Python code produced by senior_engineer_agent in response to the game description input.
  - reviewed_game_code: Code after QA review by qa_engineer_agent; errors fixed and issues annotated in code response (final output is the corrected python code).
  - final_game_code: Final python code for the requested game after generation, review, and evaluation steps. Example inputs available in src/game_builder_crew/config/gamedesign.yaml (example1_pacman, example2_pacman, example3_snake).
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task




@CrewBase
class GameBuilderCrew:
    """GameBuilderCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def senior_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_agent'],
        )

    @agent
    def qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer_agent'],
        )

    @agent
    def chief_qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_qa_engineer_agent'],
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
            agent=self.senior_engineer_agent(),
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
            agent=self.qa_engineer_agent(),
            context=[self.code_task()],
        )

    @task
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_task'],
            agent=self.chief_qa_engineer_agent(),
            context=[self.review_task()],
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the GameBuilderCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
