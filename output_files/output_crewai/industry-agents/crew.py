"""
Auto-generated CrewAI Crew: BlogCrewIndustryspecializedagentsexample

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
Capabilities:
  - Vector Search: Capability to perform semantic vector search in a vector DB (Weaviate).
  - Web Search: Capability to perform web search queries using an external search API (SerperDev).
Resources:
  - weaviate_feature placeholder: Placeholder resource used in Task prompt templates: {weaviate_feature}. Represents one feature from the list of features passed into Crew.kickoff_for_each(inputs=weaviate_features).
  - MUVERA: One of the input features used in example inputs: 'MUVERA'.
  - Multi-tenancy: One of the input features used in example inputs: 'Multi-tenancy'.
  - Compliance: One of the input features used in example inputs: 'Compliance'.
  - Hybrid Search: One of the input features used in example inputs: 'Hybrid Search'.
  - WeaviateBlogChunk (Weaviate collection): Weaviate collection used as a searchable knowledge base (client.collections.get('WeaviateBlogChunk')). Represented as a beam:Instance resource.
  - BioMed Industry Analysis (expected output): Expected output: an industry-specific analysis describing why the given Weaviate feature is useful for biomedical domain.
  - Healthcare Industry Analysis (expected output): Expected output: an industry-specific analysis describing why the given Weaviate feature is useful for healthcare domain.
  - Financial Industry Analysis (expected output): Expected output: an industry-specific analysis describing why the given Weaviate feature is useful for finance domain.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


# ===========================================================
# Tool Instances
# ===========================================================
# TODO: weaviate_vector_search_tool — unknown tool class "WeaviateVectorSearchTool"
#   Description: Vector search tool configured to query a Weaviate collection (WeaviateBlogChunk)
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# weaviate_vector_search_tool = SomeCustomTool(collection_name="WeaviateBlogChunk", limit="4", weaviate_cluster_url="WCD_CLUSTER_URL (placeholder from environment/config)", weaviate_api_key="WCD_CLUSTER_KEY (placeholder secret)")
# TODO: serper_dev_tool — unknown tool class "SerperDevWebSearchTool"
#   Description: Web search tool (SerperDev) used to retrieve web search results for background r
#   Implement as a custom BaseTool or replace with a crewai_tools equivalent.
# serper_dev_tool = SomeCustomTool(verbose="True (tool verbosity flag placeholder)")



@CrewBase
class BlogCrewIndustryspecializedagentsexample:
    """BlogCrewIndustryspecializedagentsexample crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──────────────────────────────────────────

    @agent
    def biomed_agent_1(self) -> Agent:
        return Agent(
            config=self.agents_config['biomed_agent_1'],
            verbose=True,
        )

    @agent
    def healthcare_agent_1(self) -> Agent:
        return Agent(
            config=self.agents_config['healthcare_agent_1'],
            verbose=True,
        )

    @agent
    def financial_agent_1(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_agent_1'],
            verbose=True,
        )

    # ── Tasks ───────────────────────────────────────────

    @task
    def biomedical_agent_task_research_a_weaviate_feature(self) -> Task:
        return Task(
            config=self.tasks_config['biomedical_agent_task_research_a_weaviate_feature'],
            agent=self.biomed_agent_1(),
        )

    @task
    def healthcare_agent_task_research_a_weaviate_feature(self) -> Task:
        return Task(
            config=self.tasks_config['healthcare_agent_task_research_a_weaviate_feature'],
            agent=self.healthcare_agent_1(),
        )

    @task
    def financial_agent_task_research_a_weaviate_feature(self) -> Task:
        return Task(
            config=self.tasks_config['financial_agent_task_research_a_weaviate_feature'],
            agent=self.financial_agent_1(),
        )

    # ── Crew ────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the BlogCrewIndustryspecializedagentsexample"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
