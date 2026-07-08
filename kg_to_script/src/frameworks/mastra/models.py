"""
Layer 2 – Pydantic Intermediate Representation (IR) for Mastra AI

Strongly-typed data models that sit between SPARQL extraction (Layer 1)
and TypeScript file generation (Layer 3). Every field maps to a concrete
Mastra AI TypeScript construct, making the pipeline deterministic and testable.

Mapping overview:
    KG :Team           → MastraProject      → index.ts (new Mastra({...}))
    KG :LLMAgent       → MastraAgentModel   → agents/{agent}.ts
    KG :Tool           → MastraToolModel    → tools/{tool}.ts (createTool)
    KG :WorkflowPattern → WorkflowModel     → workflows/{workflow}.ts
    KG :WorkflowStep   → StepModel          → createStep in workflow
    KG :Memory         → MemoryModel        → Memory instance config
    KG :LanguageModel  → LanguageModelModel → model router string
    KG :Config         → ConfigModel        → .env / config objects
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from src.core.models import TaskModel


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class ControlFlowType(str, Enum):
    """Mastra workflow control flow type."""
    SEQUENTIAL = "sequential"        # .then(step)
    PARALLEL = "parallel"            # .parallel([step1, step2])
    BRANCHING = "branching"          # .branch(condition, stepA, stepB)
    LOOP = "loop"                    # .doUntil(condition, step)
    MIXED = "mixed"                  # Combination of above


# ──────────────────────────────────────────────
# Leaf Models
# ──────────────────────────────────────────────

class ConfigModel(BaseModel):
    """A single key-value configuration entry from KG :Config."""
    key: str = Field(..., description="Config key (e.g. 'model', 'api_key', 'maxRetries')")
    value: str = Field(..., description="Config value")


class LanguageModelModel(BaseModel):
    """
    Represents a KG :LanguageModel (LLM backing agents).
    
    Maps to Mastra model router string format: 'provider/model-name'
    Example: 'openai/gpt-4o', 'anthropic/claude-3-5-sonnet-20241022'
    """
    iri: str = Field(..., description="Full IRI of the LanguageModel individual")
    name: str = Field("", description="Human-readable name / label (e.g. 'openai:gpt-4o')")
    description: str = Field("", description="dcterms:description text")
    provider: str = Field("", description="Provider (e.g. 'openai', 'anthropic', 'google')")
    model_name: str = Field("", description="Model identifier (e.g. 'gpt-4o', 'claude-3-5-sonnet')")
    
    @property
    def model_router_string(self) -> str:
        """
        Generate Mastra model router string.
        Format: 'provider/model-name'
        """
        if self.provider and self.model_name:
            return f"{self.provider}/{self.model_name}"
        # Fallback: try to parse from name
        if self.name and (":" in self.name or "/" in self.name):
            return self.name.replace(":", "/")
        return self.model_name or "openai/gpt-4o"  # default


class ToolConfigModel(BaseModel):
    """Tool-specific configuration entry."""
    key: str = Field(..., description="Config key (e.g. 'url', 'api_endpoint')")
    value: str = Field(..., description="Config value")


# ──────────────────────────────────────────────
# Tool Model
# ──────────────────────────────────────────────

class MastraToolModel(BaseModel):
    """
    Represents a KG :Tool → Mastra createTool().

    Maps to:
      - tools/{tool_var_name}.ts with createTool() definition
      - inputSchema/outputSchema as Zod schemas
      - execute function with TODO implementation
    """
    iri: str = Field(..., description="Full IRI of the Tool individual")
    var_name: str = Field(..., description="TypeScript variable name (camelCase)")
    tool_id: str = Field(..., description="Tool ID (from rdfs:label)")
    description: str = Field("", description="Tool description")
    
    # Schema fields (parsed from KG descriptions)
    input_schema: Optional[str] = Field(
        None, 
        description="Zod input schema string (e.g. 'z.object({ city: z.string() })')"
    )
    output_schema: Optional[str] = Field(
        None, 
        description="Zod output schema string"
    )
    
    # Execution logic (as description for TODO comment)
    execute_description: str = Field(
        "", 
        description="Description of tool execution logic (from KG description)"
    )
    
    configs: List[ToolConfigModel] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    is_custom: bool = Field(
        True, 
        description="True = needs manual implementation (default for Mastra)"
    )
    is_storage_tool: bool = Field(
        False,
        description="True = tool is a storage backend, skip createTool() generation"
    )


# ──────────────────────────────────────────────
# Agent Model
# ──────────────────────────────────────────────

class MastraAgentModel(BaseModel):
    """
    Represents a KG :LLMAgent → Mastra Agent.

    Maps to:
      - agents/{agent_var_name}.ts
      - new Agent({ id, name, instructions, model, tools })
    """
    iri: str = Field(..., description="Full IRI")
    var_name: str = Field(..., description="TypeScript variable name (camelCase)")
    agent_id: str = Field(..., description=":agentID literal")
    name: str = Field("", description="Human-readable name (rdfs:label or dcterms:title)")
    
    # Core Mastra Agent properties
    instructions: str = Field(
        ..., 
        description="Agent instructions (from :agentPrompt → :promptInstruction)"
    )
    model: str = Field(
        "openai/gpt-4o", 
        description="Model router string (e.g. 'openai/gpt-4o')"
    )
    
    # Tools & Memory
    tool_var_names: List[str] = Field(
        default_factory=list, 
        description="Tool variable names to import and use"
    )
    memory_var_name: Optional[str] = Field(
        None, 
        description="Memory instance variable name (if :hasKnowledge present)"
    )
    
    # Optional configurations
    max_retries: Optional[int] = Field(
        None, 
        description="Max retries (from :hasAgentConfig)"
    )
    
    # Store full LLM model object for reference
    llm: Optional[LanguageModelModel] = Field(
        None, 
        description="Full language model object (for provider detection)"
    )


# ──────────────────────────────────────────────
# Step Model (Workflow Step)
# ──────────────────────────────────────────────

class StepModel(BaseModel):
    """
    Represents a KG :WorkflowStep → Mastra createStep().

    Maps to createStep() call in workflow file with:
      - id, inputSchema, outputSchema
      - execute: async ({ inputData }) => { ... }
    """
    iri: str = Field(..., description="Full IRI")
    var_name: str = Field(..., description="TypeScript variable name (camelCase)")
    step_id: str = Field(..., description="Step ID (from rdfs:label or dcterms:title)")
    step_order: int = Field(..., description="Integer step order")
    description: str = Field("", description="Step description")
    
    # Schemas (parsed from :taskPrompt → Prompt properties)
    input_schema: Optional[str] = Field(
        None, 
        description="Zod input schema (from :promptInputData)"
    )
    output_schema: Optional[str] = Field(
        None,
        description="Zod output schema (from :promptOutputIndicator)"
    )

    # Field names parsed out of input_schema/output_schema (post schema-chaining
    # in generator.py) for use in execute() body codegen — Jinja can't easily
    # parse a raw "z.object({a: z.string(), b: z.string()})" string itself.
    input_fields: List[str] = Field(default_factory=list)
    output_fields: List[str] = Field(default_factory=list)

    # Execution logic
    execute_description: str = Field(
        "", 
        description="Step execution description (from :promptInstruction or task description)"
    )
    
    # References to other entities
    task_iri: Optional[str] = Field(
        None,
        description="IRI of the associated task"
    )
    agent_var_name: Optional[str] = Field(
        None, 
        description="Agent var_name if step uses an agent"
    )
    tool_var_name: Optional[str] = Field(
        None, 
        description="Tool var_name if step uses a tool"
    )
    
    # Suspend/resume support
    is_suspend_resume: bool = Field(
        False, 
        description="True if step supports suspend/resume"
    )
    suspend_schema: Optional[str] = Field(
        None, 
        description="Suspend schema (Zod) — data passed to suspend()"
    )
    resume_schema: Optional[str] = Field(
        None, 
        description="Resume schema (Zod) — resumeData shape"
    )
    suspend_message: Optional[str] = Field(
        None,
        description="Human-readable message passed to suspend() call"
    )

    # Branching support (Milestone 4)
    condition: Optional[str] = Field(
        None,
        description="Branch condition expression (e.g. 'gatherCandidateInfo.isTechnical == true')"
    )
    after_step_var_name: Optional[str] = Field(
        None,
        description="If set, this step must be preceded by .after(stepVarName) in the workflow chain"
    )


# ──────────────────────────────────────────────
# Workflow Model
# ──────────────────────────────────────────────

class WorkflowModel(BaseModel):
    """
    Represents a KG :WorkflowPattern → Mastra Workflow.

    Maps to:
      - workflows/{workflow_var_name}.ts
      - new Workflow({ name, triggerSchema })
        .step(step1).then(step2)...commit()
    
    Control flow:
      SEQUENTIAL  → .step(s1).then(s2).then(s3).commit()
      BRANCHING   → .step(s1).then(s2, {when:...}).after(s1).step(s3, {when:...}).commit()
      PARALLEL    → .step(s1).then(s2).step(s3).step(s4).commit()
      LOOP        → .step(s1).then(s2, {when:...}).after(s1).step(s1, {when:...}).commit()
    """
    iri: str = Field(..., description="Full IRI")
    var_name: str = Field(..., description="TypeScript variable name (camelCase)")
    workflow_id: str = Field(..., description="Workflow ID (from rdfs:label)")
    description: str = Field("", description="Workflow description")

    # Schemas (trigger / output)
    input_schema: Optional[str] = Field(
        None,
        description="Workflow trigger Zod schema (triggerSchema)"
    )
    output_schema: Optional[str] = Field(
        None,
        description="Workflow output Zod schema"
    )

    # Steps
    steps: List[StepModel] = Field(
        default_factory=list,
        description="Ordered list of workflow steps"
    )

    # Control flow
    control_flow: ControlFlowType = Field(
        ControlFlowType.SEQUENTIAL,
        description="Workflow control flow type"
    )

    # Nested sub-workflows this workflow contains (used as steps)
    nested_workflow_var_names: List[str] = Field(
        default_factory=list,
        description="Variable names of nested sub-workflows invoked as steps"
    )


# ──────────────────────────────────────────────
# Memory Model
# ──────────────────────────────────────────────

class MemoryModel(BaseModel):
    """
    Represents a KG :Memory → Mastra Memory config.

    Maps to Memory instance with storage backend:
      new Memory({ storage: new MongoDBStore({...}), options: {...} })
    
    KG config keys are parsed into typed fields:
      "lastMessages"                  → last_messages
      "semanticRecall.topK"           → semantic_recall_top_k
      "semanticRecall.messageRange"   → semantic_recall_message_range
      "semanticRecall" = "false"      → semantic_recall_enabled = False
      "workingMemory.enabled"         → working_memory_enabled
      "workingMemory.template"        → working_memory_template
      "workingMemory.scope"           → working_memory_scope
      "embedder" / "memory.embedder.model" → embedder_model
      "TokenLimiter"                  → token_limit
      "memory.storage.*"              → storage_type + storage_config
      "memory.vector.*"               → vector_type + vector_config
    """
    iri: str = Field(..., description="Full IRI")
    var_name: str = Field(..., description="TypeScript variable name (camelCase)")
    label: str = Field("", description="Memory label/name")
    description: str = Field("", description="Memory description")

    # ── Storage backend ──
    storage_type: str = Field(
        "libsql",
        description="Storage backend: 'mongodb' | 'libsql' | 'pg' | 'upstash'"
    )
    storage_config: List[ConfigModel] = Field(
        default_factory=list,
        description="Storage-specific key-value pairs (url, dbName, connectionString…)"
    )

    # ── Vector store (optional, used for semantic recall) ──
    vector_type: Optional[str] = Field(
        None,
        description="Vector backend: 'pgvector' | 'mongodbvector' | 'upstash-vector' | None"
    )
    vector_config: List[ConfigModel] = Field(
        default_factory=list,
        description="Vector store config (connectionString, etc.)"
    )

    # ── Embedder ──
    embedder_model: Optional[str] = Field(
        None,
        description="Embedder model string (e.g. 'openai.embedding(\"text-embedding-3-small\")')"
    )

    # ── Memory options ──
    last_messages: Optional[int] = Field(
        None,
        description="Number of recent messages to keep (options.lastMessages)"
    )
    semantic_recall_enabled: bool = Field(
        True,
        description="Whether semantic recall is enabled (false if 'semanticRecall' = 'false')"
    )
    semantic_recall_top_k: Optional[int] = Field(
        None,
        description="Top-K results for semantic recall (options.semanticRecall.topK)"
    )
    semantic_recall_message_range: Optional[int] = Field(
        None,
        description="Message range for semantic recall (options.semanticRecall.messageRange)"
    )
    working_memory_enabled: bool = Field(
        False,
        description="Enable working memory (options.workingMemory.enabled)"
    )
    working_memory_template: Optional[str] = Field(
        None,
        description="Working memory template string (options.workingMemory.template)"
    )
    working_memory_scope: Optional[str] = Field(
        None,
        description="Working memory scope: 'resource' | 'thread' (options.workingMemory.scope)"
    )
    token_limit: Optional[int] = Field(
        None,
        description="Token limit for TokenLimiter processor"
    )

    # ── Legacy / raw semantic_recall dict (kept for backward compat) ──
    semantic_recall: Optional[Dict[str, int]] = Field(
        None,
        description="Aggregated semantic recall config dict (built during extraction)"
    )


# ──────────────────────────────────────────────
# Top-level Project Model
# ──────────────────────────────────────────────

class MastraProject(BaseModel):
    """
    Complete intermediate representation for one Mastra AI project.

    This is the single data structure passed from Layer 1 → Layer 3.
    It contains all information needed to generate:
      - src/mastra/index.ts (Mastra instance)
      - src/mastra/agents/{agent}.ts
      - src/mastra/tools/{tool}.ts
      - src/mastra/workflows/{workflow}.ts
      - package.json
      - tsconfig.json
      - .env.example
    """
    # Project metadata
    project_name: str = Field(..., description="PascalCase project name (e.g. 'QuickStart')")
    project_var_name: str = Field(..., description="kebab-case directory name (e.g. 'quick-start')")
    description: str = Field("", description="Project description from Team")
    output_profile: str = Field(
        "mastra_core",
        description="Output layout profile (e.g. mastra_core, app_scaffold)",
    )
    
    # Components
    agents: List[MastraAgentModel] = Field(default_factory=list)
    tools: List[MastraToolModel] = Field(default_factory=list)
    workflows: List[WorkflowModel] = Field(default_factory=list)
    tasks: List[TaskModel] = Field(default_factory=list)
    memory_configs: List[MemoryModel] = Field(default_factory=list)
    
    # Language models (for dependency detection)
    language_models: List[LanguageModelModel] = Field(default_factory=list)
    
    # Environment variables
    env_vars: List[ConfigModel] = Field(
        default_factory=list, 
        description="Environment variables (API keys etc.)"
    )
    
    # System configs
    system_configs: List[ConfigModel] = Field(
        default_factory=list, 
        description="System-level configs (logger, etc.)"
    )

    # New ontology fields
    goals: List[dict] = Field(default_factory=list, description="Team Goals extracted from KG")
    objectives: List[dict] = Field(default_factory=list, description="Objectives extracted from KG")
    human_agents: List[dict] = Field(default_factory=list, description="HumanAgent individuals")
    environments: List[dict] = Field(default_factory=list, description="Environment individuals")
    capabilities: List[dict] = Field(default_factory=list, description="Capability individuals")
    resources: List[dict] = Field(default_factory=list, description="Resource individuals")
    constraints: List[dict] = Field(default_factory=list, description="Constraint individuals")


MastraProject.model_rebuild()
