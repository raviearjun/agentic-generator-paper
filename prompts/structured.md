<!-- P2: STRUCTURED
Changes from baseline:
- Added explicit enumeration of all 21 ontology classes with descriptions
- Added explicit enumeration of all 41 object properties with domain/range hints
- Added explicit enumeration of all 13 data properties
- Added a mandatory extraction checklist per entity type
- All other instructions identical to baseline
Hypothesis: More consistent use of correct classes/properties, fewer wrong-class assignments, better relationship coverage.
-->

You are an expert in agent systems and ontology population.

You will be given:
1) An existing ontology file in Turtle format (http://www.w3id.org/agentic-ai/onto)
{{ontology}}
2) The source code and configuration of an agent-based solution (with agents, tasks, tools, workflows, prompts, etc.)
{{source_code}}

---

## Ontology Reference

The ontology defines exactly the following classes and properties. Use ONLY these — do not invent new ones.

### Classes (21 domain classes)
| Class | Use for |
|-------|---------|
| `:LLMAgent` | Any LLM-backed agent (AssistantAgent, CrewAgent, LangGraph node with LLM, etc.) |
| `:HumanAgent` | Human-in-the-loop participants |
| `:Team` | A group of agents (Crew, GroupChat, StateGraph, etc.) |
| `:Task` | A unit of work assigned to an agent |
| `:Tool` | A callable function or external service used by an agent |
| `:WorkflowPattern` | A high-level workflow structure (sequential, hierarchical, parallel, etc.) |
| `:WorkflowStep` | A single step within a workflow |
| `:StartStep` | The first step of a workflow (subclass of WorkflowStep) |
| `:EndStep` | The last step of a workflow (subclass of WorkflowStep) |
| `:Prompt` | A prompt template, system message, or instruction text |
| `:Goal` | A high-level objective for an agent or team |
| `:Objective` | A specific measurable target |
| `:Capability` | An abstract skill or capability an agent possesses |
| `:Config` | A key-value configuration entry |
| `:Constraint` | A restriction or condition |
| `:Context` | Runtime context or environment state |
| `:Memory` | Memory storage for agents |
| `:KnowledgeBase` | A structured knowledge store |
| `:LanguageModel` | An LLM (e.g., gpt-4o, llama3) |
| `:Environment` | Execution environment |
| `:Instance` | A running instance of an agent solution |

### Key Object Properties
| Property | Connects |
|----------|----------|
| `:hasAgentMember` | Team → LLMAgent/HumanAgent |
| `:performedByAgent` | Task → LLMAgent |
| `:agentToolUsage` | LLMAgent → Tool |
| `:hasWorkflowStep` | WorkflowPattern → WorkflowStep |
| `:hasAssociatedTask` | WorkflowStep → Task |
| `:nextStep` | WorkflowStep → WorkflowStep |
| `:hasWorkflowPattern` | Team → WorkflowPattern |
| `:agentPrompt` | LLMAgent → Prompt |
| `:taskPrompt` | Task → Prompt |
| `:useLanguageModel` | LLMAgent → LanguageModel |
| `:hasAgentConfig` | LLMAgent → Config |
| `:hasToolConfig` | Tool → Config |
| `:hasAgentGoal` | LLMAgent → Goal |
| `:hasTeamGoal` | Team → Goal |
| `:interactsWith` | LLMAgent → LLMAgent/HumanAgent |
| `:producedResource` | Task → resource individual |
| `:requiresResource` | Task → resource individual |
| `:hasSubPattern` | WorkflowPattern → WorkflowPattern |
| `:nextPattern` | WorkflowPattern → WorkflowPattern |
| `:hasCapability` | Tool/LLMAgent → Capability |

### Key Data Properties
| Property | Use for |
|----------|---------|
| `:agentID` | Agent identifier string |
| `:agentRole` | Agent role label |
| `:promptInstruction` | Actual instruction text of a prompt |
| `:promptContext` | Background context of a prompt |
| `:promptOutputIndicator` | Expected output description |
| `:promptInputData` | Input data specification |
| `:configKey` | Config key string |
| `:configValue` | Config value string |
| `:stepOrder` | Integer step order |
| `dcterms:title` | Human-readable name |
| `dcterms:description` | Detailed description |

---

## Mandatory Extraction Checklist

For **every agent** extract:
- [ ] `:LLMAgent` or `:HumanAgent` individual
- [ ] `:agentID` (name/identifier)
- [ ] `:agentRole` (role description)
- [ ] `:agentPrompt` → `:Prompt` with `:promptInstruction` (system message)
- [ ] `:useLanguageModel` → `:LanguageModel` if LLM is specified
- [ ] `:agentToolUsage` for every tool the agent uses
- [ ] `:hasAgentGoal` → `:Goal` if a goal is specified

For **every task** extract:
- [ ] `:Task` individual
- [ ] `:performedByAgent` → agent
- [ ] `:taskPrompt` → `:Prompt` with `:promptInstruction` (task description) and `:promptOutputIndicator` (expected output)
- [ ] `:requiresResource` / `:producedResource` for data dependencies

For **every tool** extract:
- [ ] `:Tool` individual
- [ ] `:hasCapability` → `:Capability` describing what it does
- [ ] `:hasToolConfig` for any configuration parameters

For **workflow** extract:
- [ ] `:WorkflowPattern` with type (sequential/hierarchical)
- [ ] `:StartStep`, `:WorkflowStep`, `:EndStep` with `:stepOrder`
- [ ] `:hasAssociatedTask` linking each step to a task
- [ ] `:nextStep` chain

For **team/group** extract:
- [ ] `:Team` individual
- [ ] `:hasAgentMember` for every agent
- [ ] `:hasWorkflowPattern` linking to the workflow

---

## Instructions

1. Study the ontology file.
   - Treat it as a fixed schema with all classes and properties already defined.
   - Do NOT add, modify, or remove any classes or properties in the schema!

2. Study the source code and configuration.
   - Extract all instance-level information needed to fully describe the solution.

3. Populate the ontology using the checklist above as guidance.
   - Use ONLY the existing classes and properties listed above.
   - Create individuals for all relevant entities and connect them with the appropriate properties.
   - Preserve all information from the source code (including prompts, parameters, and important logic) as literals.
   - Fidelity is important — do not change or condense information.

4. If some aspects cannot be modeled:
   - Do NOT invent new classes or properties.
   - Model as closely as possible without abusing the schema.
   - List missing concepts in the "Issues / Assumptions" comment block.

Output format:

- Respond with the instance information in .ttl format.
- At the very top of the Turtle content, write a comment block:

  Issues / Assumptions:
  - <issue 1 or "No issues detected">
  - <issue 2>
  ...

  Do not ask for confirmation or clarifications, just produce the output as specified.

IMPORTANT: Output raw Turtle only. Do NOT wrap in markdown code fences. Do NOT add explanations before or after the Turtle. Start your response with @prefix or # and end with the last triple.
