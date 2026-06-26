<!-- P3: REASONING
Changes from baseline:
- Added mandatory two-phase approach: first reason/plan (Phase 1), then generate TTL (Phase 2)
- Phase 1 requires structured analysis of agents, tasks, tools, workflow, and LLMs before writing any Turtle
- All constraints and output format instructions identical to baseline
Hypothesis: Chain-of-thought reasoning reduces semantic mapping errors and improves extraction of implicit relationships.
-->

You are an expert in agent systems and ontology population.

You will be given:
1) An existing ontology file in Turtle format (http://www.w3id.org/agentic-ai/onto)
{{ontology}}
2) The source code and configuration of an agent-based solution (with agents, tasks, tools, workflows, prompts, etc.)
{{source_code}}

---

## Two-Phase Approach

### Phase 1 — Reasoning (required before generating Turtle)

Before writing any Turtle, reason through the following questions and write your analysis as a comment block at the top of the output under the heading `# REASONING`:

**A. Framework Structure**
- What agentic framework is this? (CrewAI / LangGraph / AutoGen / other)
- What is the high-level purpose of the system?
- What is the team/group structure?

**B. Agents**
- List every agent with: name, role, system message / prompt, assigned LLM, tools used.
- Identify which agents are LLM-based vs human proxies.
- Note any agent-to-agent interaction patterns.

**C. Tasks**
- List every task with: name, description, expected output, assigned agent.
- Note data flow dependencies between tasks (which task's output feeds which task's input).

**D. Tools**
- List every tool with: name, description, parameters, capabilities.

**E. Workflow**
- Describe the execution order of tasks/agents.
- Identify the workflow pattern type: sequential, hierarchical, parallel, reflection, or nested.
- Map step order numbers to tasks.

**F. Ontology Mapping Decisions**
- For each major concept, state which ontology class you will use and why.
- Flag any concepts that have no clear ontology mapping.

---

### Phase 2 — Turtle Generation

After completing the reasoning, generate the Turtle (.ttl) ontology population following these rules:

1. Study the ontology file.
   - Treat it as a fixed schema with all classes and properties already defined.
   - Do NOT add, modify, or remove any classes or properties in the schema!

2. Use the reasoning from Phase 1 to ensure every entity is correctly typed and linked.
   - Populate the ontology with individuals based on the extracted information.
   - Use ONLY the existing classes and properties from the ontology.
   - Create individuals for all relevant entities and connect them with the appropriate properties.
   - Preserve all information from the source code (including prompts, parameters, and important logic) as literals or links between individuals. Fidelity is important, do not change or condense information.

3. If some aspects of the solution cannot be modeled with the current ontology:
   - Do NOT invent new classes or properties!
   - Do NOT model programming information (e.g., specific code structures, language-specific constructs, or implementation details).
   - Model them as closely as possible with the existing schema but do not abuse the schema.
   - List any missing concepts in the "Issues / Assumptions" comment block.

Output format:

- Respond with the instance information in .ttl format.
- Structure your output as follows:

```
# REASONING
# A. Framework Structure: ...
# B. Agents: ...
# C. Tasks: ...
# D. Tools: ...
# E. Workflow: ...
# F. Ontology Mapping Decisions: ...

# Issues / Assumptions:
# - <issue 1 or "No issues detected">

@prefix : <http://www.w3id.org/agentic-ai/onto#> .
...
```

Do not ask for confirmation or clarifications, just produce the output as specified.

IMPORTANT: Output raw Turtle only. Do NOT wrap in markdown code fences. Do NOT add explanations before or after the Turtle. Start your response with @prefix or # and end with the last triple.
