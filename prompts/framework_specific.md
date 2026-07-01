<!-- P5: FRAMEWORK-SPECIFIC
Changes from P2 (structured):
- Added automatic framework detection step before any extraction
- Added per-framework extraction rules (CrewAI / LangGraph / AutoGen / Mastra AI)
  with exact mapping from framework constructs to ontology classes/properties
- Added mandatory Tool extraction rule (create :Tool for every external function/API)
- Added mandatory LanguageModel rule (create :LanguageModel even when implicit)
- Added mandatory StartStep/EndStep rule
- Added mandatory interactsWith extraction for multi-agent conversations
- Retained full P2 class/property reference and extraction checklist
- Added post-generation completeness check targeting the most commonly missing elements
Hypothesis: Framework-specific mapping guidance plus targeted gap-filling pushes macro F1 above 0.85.
-->

You are an expert in agent systems and ontology population.

You will be given:
1) An existing ontology file in Turtle format (http://www.w3id.org/agentic-ai/onto)
{{ontology}}
2) The source code and configuration of an agent-based solution (with agents, tasks, tools, workflows, prompts, etc.)
{{source_code}}

---

## Step 0 — Detect the Framework

Before extracting anything, identify which agentic framework the source code uses. Look for these signals:

| Signal in code | Framework |
|----------------|-----------|
| `from crewai import`, `@agent`, `@task`, `@tool`, `Crew(`, `Process.` | **CrewAI** |
| `from langgraph`, `StateGraph(`, `add_node(`, `add_edge(`, `add_conditional_edges(` | **LangGraph** |
| `from autogen`, `AssistantAgent(`, `UserProxyAgent(`, `ConversableAgent(`, `GroupChat(` | **AutoGen** |
| `from @mastra`, `new Agent(`, `new Workflow(`, `.step(`, `mastra.getAgent` | **Mastra AI** |

Write the detected framework as the first comment line in your output:
```
# Framework: <CrewAI | LangGraph | AutoGen | Mastra AI | Other>
```

Then apply the framework-specific extraction rules below.

---

## Framework-Specific Extraction Rules

### CrewAI Rules

Map every CrewAI construct as follows:

| CrewAI construct | Ontology mapping |
|-----------------|-----------------|
| `@agent` decorated function or `Agent(role=..., goal=..., backstory=...)` | `:LLMAgent` with `:agentRole`, `:agentID`, `:hasAgentGoal → :Goal` |
| `agent.backstory` / `agent.goal` | `:agentPrompt → :Prompt` with `:promptInstruction` |
| `@task` decorated function or `Task(description=..., expected_output=...)` | `:Task` with `:taskPrompt → :Prompt` (description in `:promptInstruction`, expected_output in `:promptOutputIndicator`) |
| `task.agent` / `agent=` parameter | `:performedByAgent → :LLMAgent` |
| `@tool` decorated function or `SerperDevTool()`, any imported Tool class | `:Tool` individual; link agent via `:agentToolUsage → :Tool` |
| `agent.tools = [...]` | For each tool: `:agentToolUsage → :Tool` |
| `Agent(llm=...)` or environment default LLM | `:LanguageModel` individual; link via `:useLanguageModel → :LanguageModel` (create one even if only env var is set) |
| `Crew(agents=[...], tasks=[...])` | `:Team` with `:hasAgentMember` for every agent, `:hasTeamGoal → :Goal` |
| `Process.sequential` | `:WorkflowPattern` with `dcterms:title "Sequential"` |
| `Process.hierarchical` | `:WorkflowPattern` with `dcterms:title "Hierarchical"` |
| Task execution order (position in `tasks=[t1, t2, ...]`) | `:WorkflowStep` individuals with `:stepOrder`, linked as `:StartStep` (first), `:EndStep` (last), chained via `:nextStep` |
| `Crew.kickoff_inputs` / input variables | `:Config` on team with key/value |
| `max_iter`, `max_rpm`, `verbose`, `memory` on Agent | `:Config` individuals on `:LLMAgent` via `:hasAgentConfig` |
| `config/agents.yaml` or any agent config file (if present) | For each key in the agent's config block (e.g., `max_iter`, `verbose`, `allow_delegation`, `cache`): one `:Config` individual per key with `:configKey` and `:configValue`; link to the agent via `:hasAgentConfig` |

### LangGraph Rules

Map every LangGraph construct as follows:

| LangGraph construct | Ontology mapping |
|--------------------|-----------------|
| `StateGraph(State)` | `:WorkflowPattern` with `dcterms:title "StateGraph"` |
| `graph.add_node("name", function)` | `:WorkflowStep` individual (IRI matches node name); also `:Task` individual linked via `:hasAssociatedTask` |
| LLM-calling node (uses `llm.invoke`, `model.invoke`) | `:LLMAgent` individual linked to the WorkflowStep |
| `graph.add_edge(A, B)` | `:nextStep` triple: step_A `:nextStep` step_B |
| `graph.add_conditional_edges(node, router, {k: v})` | `:nextStep` triples for each possible target; describe routing in `:Prompt.promptInstruction` on the router step |
| `START` constant | `:StartStep` individual |
| `END` constant | `:EndStep` individual |
| `model.bind_tools([...])` or `ToolNode([...])` | `:Tool` for each tool; `:agentToolUsage → :Tool` on the calling `:LLMAgent` |
| `ChatAnthropic(...)`, `ChatOpenAI(...)`, `init_chat_model(...)` | `:LanguageModel` with `dcterms:title` = model name |
| `agent.invoke(state)` / `model.invoke(messages)` | `:Task` with `:performedByAgent` |
| `SystemMessage(content=...)` / `system_prompt` | `:Prompt` with `:promptInstruction` linked via `:agentPrompt` |
| `StateGraph` as top-level team | `:Team` with `:hasWorkflowPattern` |
| `MemorySaver()`, `checkpointer=` | `:Memory` individual linked via `:hasKnowledge` |

### AutoGen Rules

Map every AutoGen construct as follows:

| AutoGen construct | Ontology mapping |
|------------------|-----------------|
| `AssistantAgent(name=..., system_message=...)` | `:LLMAgent` with `:agentID`, `:agentRole`, `:agentPrompt → :Prompt` (system_message in `:promptInstruction`) |
| `UserProxyAgent(name=...)` | `:HumanAgent` individual (or `:LLMAgent` if `human_input_mode="NEVER"`) |
| `ConversableAgent` | `:LLMAgent` |
| `llm_config = {"model": "...", "temperature": ...}` | `:LanguageModel` individual; `:useLanguageModel`; additional keys as `:Config` via `:hasAgentConfig` |
| `@agent.register_for_llm()` / `@agent.register_for_execution()` / `register_function(fn, ...)` | `:Tool` individual for each registered function; `:agentToolUsage → :Tool` on the registering agent |
| `agent.initiate_chat(recipient, message=..., max_turns=...)` | `:Task` individual; `:performedByAgent`; `:taskPrompt → :Prompt` (message in `:promptInstruction`); `max_turns` as `:Config` |
| Agent A initiates chat with Agent B | `:interactsWith` triple: agentA `:interactsWith` agentB (and agentB `:interactsWith` agentA for bidirectional) |
| `initiate_chats([{...}, {...}])` sequential chats | Multiple `:Task` individuals linked as `:WorkflowStep` with `:nextStep` chain |
| `GroupChat(agents=[...], messages=[], max_round=...)` | `:Team` with `:hasAgentMember` for all agents; `max_round` as `:Config` |
| `GroupChatManager(groupchat=..., llm_config=...)` | `:LLMAgent` as manager with `:agentRole "GroupChatManager"` |
| Nested chat / `register_nested_chats` | `:WorkflowPattern` with `dcterms:title "Nested"` + `:WorkflowStep` individuals |
| `is_termination_msg`, `max_consecutive_auto_reply` | `:Config` on the relevant `:LLMAgent` |
| Any external config dict / JSON file passed to an agent (e.g., `llm_config`, `code_execution_config`) | Extract each key-value pair as a `:Config` individual linked via `:hasAgentConfig` |

### Mastra AI Rules

Map every Mastra AI construct as follows:

| Mastra AI construct | Ontology mapping |
|--------------------|-----------------|
| `new Agent({ name, instructions, model, tools })` | `:LLMAgent` with `:agentID` (name), `:agentPrompt → :Prompt` (instructions in `:promptInstruction`) |
| `model: openai('gpt-4o')` / `anthropic('claude-3-5-sonnet')` | `:LanguageModel` with `dcterms:title` = model name; `:useLanguageModel` |
| `tools: { toolName: createTool({...}) }` | `:Tool` for each tool; `:agentToolUsage → :Tool` |
| `createTool({ id, description, execute })` | `:Tool` with `dcterms:description`; `:hasCapability → :Capability` |
| `agent.generate(prompt)` / `agent.stream(prompt)` | `:Task` with `:taskPrompt → :Prompt` (prompt text in `:promptInstruction`); `:performedByAgent` |
| `new Workflow({ name, triggerSchema })` | `:WorkflowPattern` with `dcterms:title` = name |
| `.step(stepId, { execute })` | `:WorkflowStep` with `:stepOrder`; first step as `:StartStep`, last as `:EndStep` |
| `.then(nextStepId)` / `.after(stepId)` | `:nextStep` chain |
| `workflow.commit()` | Finalises the `:WorkflowPattern` — no additional individual needed |
| `new Memory({...})` / `Memory` stores | `:Memory` individual; `:hasKnowledge → :Memory` on the agent |
| Multi-agent: `mastra.getAgent(name)` calls within a step | `:interactsWith` triples between the calling agent and the called agent |
| `new Mastra({ agents: {...} })` | `:Team` with `:hasAgentMember` for all agents |
| Any config object passed to `new Agent({...})` beyond name/instructions/model/tools (e.g., `maxSteps`, `telemetry`) | One `:Config` individual per key; link via `:hasAgentConfig` |

---

## Ontology Reference (complete)

Use ONLY these classes and properties — do not invent new ones.

### Classes
| Class | Use for |
|-------|---------|
| `:LLMAgent` | Any LLM-backed agent |
| `:HumanAgent` | Human-in-the-loop participant |
| `:Team` | Group of agents (Crew, GroupChat, StateGraph system, Mastra instance) |
| `:Task` | Unit of work assigned to an agent |
| `:Tool` | Callable function or external service used by an agent |
| `:WorkflowPattern` | High-level workflow structure |
| `:WorkflowStep` | Single step in a workflow |
| `:StartStep` | **Must use** for the first step (subclass of WorkflowStep) |
| `:EndStep` | **Must use** for the last step (subclass of WorkflowStep) |
| `:Prompt` | System message, instruction, or task description |
| `:Goal` | High-level objective for an agent or team |
| `:Objective` | Specific measurable target |
| `:Capability` | Abstract skill an agent or tool possesses |
| `:Config` | Key-value configuration entry |
| `:Constraint` | Restriction or condition on agent behaviour |
| `:Memory` | Agent memory storage |
| `:KnowledgeBase` | Structured knowledge store |
| `:LanguageModel` | An LLM (e.g., gpt-4o-mini, claude-3-5-sonnet) |
| `:Environment` | Execution environment |
| `:HumanAgent` | Human participant |

> **Never type an individual directly as `:Context`, `:Instance`, or `:KnowledgeBase` when a more specific subclass applies.**
> **Never use a property name (e.g., `:hasAgentConfig`) as the value of `rdf:type`.**

### Object Properties
| Property | Domain → Range |
|----------|---------------|
| `:hasAgentMember` | Team → LLMAgent / HumanAgent |
| `:hasWorkflowPattern` | Team → WorkflowPattern |
| `:hasWorkflowStep` | WorkflowPattern → WorkflowStep |
| `:hasAssociatedTask` | WorkflowStep → Task |
| `:nextStep` | WorkflowStep → WorkflowStep |
| `:performedByAgent` | Task → LLMAgent |
| `:agentToolUsage` | LLMAgent → Tool |
| `:useLanguageModel` | LLMAgent → LanguageModel |
| `:agentPrompt` | LLMAgent → Prompt |
| `:taskPrompt` | Task → Prompt |
| `:hasAgentConfig` | LLMAgent → Config |
| `:hasToolConfig` | Tool → Config |
| `:hasSystemConfig` | Team → Config |
| `:hasAgentGoal` | LLMAgent → Goal |
| `:hasTeamGoal` | Team → Goal |
| `:hasAgentCapability` | LLMAgent → Capability |
| `:hasCapability` | Tool → Capability |
| `:interactsWith` | LLMAgent → LLMAgent / HumanAgent |
| `:hasKnowledge` | LLMAgent → KnowledgeBase / Memory |
| `:producedResource` | Task → resource |
| `:requiresResource` | Task → resource |

### Data Properties
| Property | Domain | Use for |
|----------|--------|---------|
| `:agentID` | LLMAgent | Identifier string |
| `:agentRole` | LLMAgent | Role label |
| `:promptInstruction` | Prompt | Full instruction / description text |
| `:promptContext` | Prompt | Background context |
| `:promptOutputIndicator` | Prompt | Expected output description |
| `:promptInputData` | Prompt | Input data specification |
| `:configKey` | Config | Key string |
| `:configValue` | Config | Value string |
| `:stepOrder` | WorkflowStep | Integer ordering |
| `dcterms:title` | any | Human-readable name |
| `dcterms:description` | any | Detailed description |

---

## Mandatory Extraction Checklist

Work through this checklist for every entity in the source code.

**Agents** — for each agent create:
- [ ] `:LLMAgent` (or `:HumanAgent`) individual
- [ ] `:agentID` data property
- [ ] `:agentRole` data property
- [ ] `:agentPrompt → :Prompt` with `:promptInstruction` containing the full system message / backstory
- [ ] `:useLanguageModel → :LanguageModel` — **always create a `:LanguageModel` individual**, even when the model is set via an environment variable (use `dcterms:title "default"` if unknown)
- [ ] `:agentToolUsage → :Tool` for every tool the agent can call
- [ ] **If a config file or config dict for the agent exists** (e.g., `agents.yaml`, `llm_config`, constructor kwargs): create one `:Config` individual per key-value pair and link each via `:hasAgentConfig`

**Tools** — for each tool, API, or registered function create:
- [ ] `:Tool` individual with `dcterms:title` and `dcterms:description`
- [ ] `:hasCapability → :Capability` describing what the tool does
- [ ] `:hasToolConfig → :Config` for any parameters / API keys

**Tasks** — for each task / conversation step create:
- [ ] `:Task` individual
- [ ] `:performedByAgent → :LLMAgent`
- [ ] `:taskPrompt → :Prompt` with `:promptInstruction` (description) and `:promptOutputIndicator` (expected output)

**Workflow** — create:
- [ ] `:WorkflowPattern` individual
- [ ] `:StartStep` for the first step (typed as both `:StartStep` and `:WorkflowStep`)
- [ ] `:WorkflowStep` for every intermediate step with `:stepOrder` integer
- [ ] `:EndStep` for the last step
- [ ] `:nextStep` chain connecting every consecutive step pair
- [ ] `:hasAssociatedTask` linking each step to its task

**Team / Group** — create:
- [ ] `:Team` individual
- [ ] `:hasAgentMember` for every agent
- [ ] `:hasWorkflowPattern` linking to the workflow
- [ ] `:hasTeamGoal → :Goal` if a team-level goal is stated

**Agent Interactions** — for every pair of agents that communicate:
- [ ] `:interactsWith` triples (add in both directions for bidirectional communication)

---

## Post-Generation Completeness Check

Before writing the final output, mentally verify:

1. **Every agent** has `useLanguageModel` set (even to a default `:LanguageModel`).
2. **Every tool** mentioned in the code has a `:Tool` individual and is linked via `:agentToolUsage`.
3. **There is exactly one `:StartStep`** and **one `:EndStep`** (or one per parallel branch).
4. **Every `:WorkflowStep`** has `:stepOrder` and is connected via `:nextStep` (except the EndStep, which has no outgoing `:nextStep`).
5. **No property name is used as `rdf:type`** (e.g., never write `rdf:type :hasAgentConfig`).
6. **No individual is typed as `:Context` directly** — use `:Goal`, `:Objective`, or `:Environment` instead.
7. **Every `:Config`** has both `:configKey` and `:configValue`.
8. **Every `:Prompt`** has at least `:promptInstruction`.

---

## Output Format

- Respond with the instance information in `.ttl` format.
- Structure your output as follows:

```
# Framework: <detected framework>

# Issues / Assumptions:
# - <issue 1 or "No issues detected">

@prefix : <http://www.w3id.org/agentic-ai/onto#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix beam: <http://w3id.org/beam/core#> .

...individuals...
```

Do not ask for confirmation or clarifications, just produce the output as specified.

IMPORTANT: Output raw Turtle only. Do NOT wrap in markdown code fences. Do NOT add explanations before or after the Turtle. Start your response with # or @prefix and end with the last triple.
