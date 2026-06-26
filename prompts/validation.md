<!-- P4: VALIDATION
Changes from baseline:
- Added mandatory self-validation pass (Phase 2) after initial Turtle generation
- Self-check covers: missing agents/tasks/tools, broken links, duplicate individuals, orphaned nodes, wrong class usage, missing workflow chain
- Final output must be the validated/corrected Turtle
- All other instructions identical to baseline
Hypothesis: Post-generation self-check improves completeness and reduces structural errors and duplicate individuals.
-->

You are an expert in agent systems and ontology population.

You will be given:
1) An existing ontology file in Turtle format (http://www.w3id.org/agentic-ai/onto)
{{ontology}}
2) The source code and configuration of an agent-based solution (with agents, tasks, tools, workflows, prompts, etc.)
{{source_code}}

---

## Instructions

### Phase 1 — Generate Initial Turtle

1. Study the ontology file.
   - Treat it as a fixed schema with all classes and properties already defined.
   - Do NOT add, modify, or remove any classes or properties in the schema!

2. Study the source code and configuration.
   - Extract all instance-level information needed to fully describe the solution (agents, tasks, tools, workflows, prompts, parameters, data/artifacts, etc.).

3. Populate the ontology with individuals based on the extracted information.
   - The goal is that another LLM can reconstruct the agent solution from the ontology instances you create.
   - Use ONLY the existing classes and properties from the ontology!
   - Create individuals for all relevant entities and connect them with the appropriate properties.
   - Preserve all information from the source code (including prompts, parameters, and important logic) as literals or links between individuals. Fidelity is important, do not change or condense information.

4. If some aspects of the solution cannot be modeled with the current ontology:
   - Do NOT invent new classes or properties!
   - Do NOT model programming information, framework-specific functions, or UI components.
   - Model them as closely as possible with the existing schema but do not abuse the schema.

---

### Phase 2 — Self-Validation (required before final output)

After generating the initial Turtle, perform the following self-checks. Fix any issues found before writing the final output.

Write your validation report as a comment block under `# VALIDATION` in the output.

**Check 1 — Completeness**
- [ ] Every agent mentioned in source code has a corresponding `:LLMAgent` or `:HumanAgent` individual.
- [ ] Every task mentioned has a `:Task` individual linked to an agent via `:performedByAgent`.
- [ ] Every tool mentioned has a `:Tool` individual linked via `:agentToolUsage`.
- [ ] Every agent has a `:Prompt` individual linked via `:agentPrompt` or `:taskPrompt`.
- [ ] The team/group is represented as a `:Team` individual with `:hasAgentMember` for every agent.

**Check 2 — Workflow Integrity**
- [ ] There is at least one `:StartStep` individual.
- [ ] There is at least one `:EndStep` individual.
- [ ] All `:WorkflowStep` individuals have a `:stepOrder` value.
- [ ] Steps are linked with `:nextStep` forming a chain.
- [ ] Each step is linked to at least one task via `:hasAssociatedTask`.

**Check 3 — Structural Consistency**
- [ ] No duplicate individual IRIs (each entity has exactly one IRI).
- [ ] No orphaned individuals (every individual is connected to at least one other).
- [ ] All object property values reference defined individuals (no dangling references).
- [ ] Every `:Config` individual has both `:configKey` and `:configValue`.
- [ ] Every `:Prompt` individual has at least `:promptInstruction`.

**Check 4 — Schema Compliance**
- [ ] No new classes or properties have been introduced that are not in the ontology.
- [ ] `:LLMAgent` is not used where `:Tool` is more appropriate, and vice versa.
- [ ] `:WorkflowPattern` is not confused with `:WorkflowStep`.

For each failed check: describe what was wrong and what correction was made.

---

### Final Output

Output the **corrected** Turtle after applying all fixes.

- Respond with the instance information in .ttl format.
- Structure your output as follows:

```
# VALIDATION
# Check 1 (Completeness): PASS / issues found: ...
# Check 2 (Workflow Integrity): PASS / issues found: ...
# Check 3 (Structural Consistency): PASS / issues found: ...
# Check 4 (Schema Compliance): PASS / issues found: ...

# Issues / Assumptions:
# - <issue 1 or "No issues detected">

@prefix : <http://www.w3id.org/agentic-ai/onto#> .
...
```

Do not ask for confirmation or clarifications, just produce the output as specified.

IMPORTANT: Output raw Turtle only. Do NOT wrap in markdown code fences. Do NOT add explanations before or after the Turtle. Start your response with @prefix or # and end with the last triple.
