<!-- P1: MINIMAL
Changes from baseline:
- Removed all detailed instructions (steps 1–4)
- Removed ontology constraint warnings
- Removed output format specification
- Retained only the core extraction directive
Hypothesis: Lower concept coverage, fewer triples, higher hallucination rate due to lack of constraints.
-->

You are an expert in agent systems and ontology population.

You will be given:
1) An existing ontology file in Turtle format (http://www.w3id.org/agentic-ai/onto)
{{ontology}}
2) The source code and configuration of an agent-based solution.
{{source_code}}

Extract all agents, tasks, tools, workflows, prompts, and relationships from the source code.
Populate the ontology with individuals and output the result in Turtle (.ttl) format.

IMPORTANT: Output raw Turtle only. Do NOT wrap in markdown code fences. Do NOT add explanations before or after the Turtle. Start your response with @prefix or # and end with the last triple.
