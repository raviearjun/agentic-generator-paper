"""
Auto-generated CrewAI Crew: blogcrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Goals:
  - : Continuously track the latest biomedical advancements and identify how Weaviate’s features can support AI applications in biomedical research, diagnostics, and personalized medicine.
  - : Stay updated on healthcare policy shifts, digital health trends, and explore how Weaviate’s features can optimize workflows in hospital systems, EHR integration, and health communication.
  - : Monitor financial sector trends including AI in trading, compliance automation, and client advisory, and assess how Weaviate’s tools can enable cutting-edge financial applications.
Capabilities:
  - : Performs semantic vector search over document chunks in Weaviate.
  - : Performs web search via Serper.dev.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: tool_weaviate_vector_search_tool — unknown tool class "ToolWeaviateVectorSearchTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolWeaviateVectorSearchTool")
def tool_weaviate_vector_search_tool(*args, **kwargs) -> str:
    """Vector search tool using Weaviate for semantic retrieval from collection 'WeaviateBlogChunk'."""
    return "tool_weaviate_vector_search_tool result"

# TODO: tool_serper_dev_tool — unknown tool class "ToolSerperDevTool"
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
@tool("ToolSerperDevTool")
def tool_serper_dev_tool(*args, **kwargs) -> str:
    """Web search tool backed by Serper.dev."""
    return "tool_serper_dev_tool result"




@CrewBase
class blogcrew:
    """blogcrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def biomedical_marketing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['biomedical_marketing_agent'],
            tools=[tool_weaviate_vector_search_tool, tool_serper_dev_tool],
            verbose=True,
        )

    @agent
    def healthcare_marketing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['healthcare_marketing_agent'],
            tools=[tool_weaviate_vector_search_tool, tool_serper_dev_tool],
            verbose=True,
        )

    @agent
    def financial_marketing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_marketing_agent'],
            tools=[tool_weaviate_vector_search_tool, tool_serper_dev_tool],
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def task_biomedical_research(self) -> Task:
        return Task(
            config=self.tasks_config['task_biomedical_research'],
            agent=self.biomedical_marketing_agent(),
        )

    @task
    def task_healthcare_research(self) -> Task:
        return Task(
            config=self.tasks_config['task_healthcare_research'],
            agent=self.healthcare_marketing_agent(),
        )

    @task
    def task_financial_research(self) -> Task:
        return Task(
            config=self.tasks_config['task_financial_research'],
            agent=self.financial_marketing_agent(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the blogcrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
