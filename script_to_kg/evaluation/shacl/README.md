# SHACL shapes for generated agentic-AI KGs

Validates the KGs in `script_to_kg/generated_kgs/<Framework>/*_instances.ttl`
against the Agentic AI Ontology (`agentO.ttl`) structural rules only.

## Files

- `core.shapes.ttl` — the only shapes file. Ontology-derived structural
  shapes: object-property domain/range typing (`sh:class`), data-property
  datatypes (`sh:datatype`), and "should have" cardinality on identity/scalar
  fields (`agentID`, `agentRole`, `configKey`/`configValue`, `stepOrder`,
  ...). Type/datatype mismatches are `sh:Violation`; missing recommended
  fields are `sh:Warning`. Pure SHACL Core — no `owl:imports`, no
  SPARQL-based constraints/targets, no dependency on `evaluate_kgs.py` or any
  per-framework/per-project "expected coverage" notion.
- `generate_shapes.py` — regenerates `core.shapes.ttl`. Re-run it whenever
  `agentO.ttl` changes.
- `generate_xlsx.py` — runs `core.shapes.ttl` against the corpus and writes
  `shacl_evaluation_summary.xlsx` (same visual style/sheet convention as
  `../evaluate_kgs.py`'s output): a "Per-File Results" sheet (all 50 files,
  including the excluded/parse-error ones, clearly marked), a "Group
  Summary" sheet matching the paper's per-framework results table, and a
  "Violation & Warning Types" sheet with the property-level breakdown.
  Requires `pip install pyshacl`. Re-run after any change to `core.shapes.ttl`
  or the generated KG corpus.

## Scope note

This checks ontology **structural conformance** only — is every relation
used with the right domain/range, is every datatype correct — not whether a
given KG covers everything a human would expect from its source project
(e.g. it won't flag a KG that's missing `:Goal` entirely, only a KG that
mislabels something's type). There is deliberately no framework-specific or
project-specific "must contain at least one X" layer anymore.

## Running validation

```
pip install pyshacl

pyshacl -s script_to_kg/evaluation/shacl/core.shapes.ttl \
  "script_to_kg/generated_kgs/CrewAI/job-posting_instances.ttl"
```

No extra flags needed (no `-im`, no `-a`) — `core.shapes.ttl` is
self-contained SHACL Core.

To validate every file in the corpus at once:

```
for f in script_to_kg/generated_kgs/*/*_instances.ttl; do
  echo "== $f =="
  pyshacl -s script_to_kg/evaluation/shacl/core.shapes.ttl "$f"
done
```

## Known pre-existing data issues

A handful of generated `.ttl` files contain unescaped quotes/newlines inside
Turtle string literals and fail to parse with rdflib/pyshacl before SHACL
validation even runs — a Turtle syntax defect in those generated files, not
something these shapes check for.

## Excluded projects (SHACL only)

`LangGraph/open-code`, `stockbroker`, `trip-planner`, and `Mastra AI/a2a`,
`agent1`, `mcp-registry-registry` still have a `.ttl` file in
`generated_kgs/` — they're used by every other evaluation in the paper
(completeness/Macro F1, prompt ablation, model comparison, code-generation
SCR/ER/CCR/WGI/CFCS), which deliberately keep the full, unfiltered
repository-declared example set. **Only the SHACL evaluation excludes
them**, via the `EXCLUDED` set in `generate_xlsx.py` (and the equivalent
manual filtering if you run `pyshacl` ad hoc) — not by removing the files.
Reasoning: SHACL checks whether a KG's triples are semantically well-typed
relative to the ontology, and for these six there is no genuine agentic
implementation in the source for the ontology to represent in the first
place (the three LangGraph ones have no backend source, only frontend UI
components; the three Mastra AI ones are SDK/protocol client-wrapper
classes, not concrete `Agent`/`Tool`/`Team`/`Workflow` definitions) — so
validating the internal type-consistency of whatever near-empty or
unsubstantiated RDF the model produced for them isn't a meaningful test of
the ontology's fitness. See `evaluation.tex`, section `eval-shacl`, for the
full argument and citations.
