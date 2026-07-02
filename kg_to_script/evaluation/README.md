# OEC/WGI Evaluation

Run from `kg_to_script/`:

```bash
python -m evaluation.run
```

Or from the repository root:

```bash
python -m kg_to_script.evaluation.run
```

Optional framework filter:

```bash
python -m evaluation.run --framework crewai
python -m evaluation.run --framework autogen
python -m evaluation.run --framework langgraph
python -m evaluation.run --framework mastra
```

Outputs are written to `evaluation_results/` by default:

- `oec_wgi_results.json` for machine-readable analysis
- `oec_wgi_results.md` for a human-readable report

## OEC Denominators

- `all_extracted`: denominator includes all ontology elements extracted into the canonical IR, including supporting goals, capabilities, resources, constraints, configs, and relations.
- `important_subset`: denominator includes core implementation-critical elements, mainly agents, tasks, tools, workflow steps, core workflow relations, and important config keys such as process, model, temperature, max loops/messages/turns, verbose, memory, and human input.

Use `all_extracted` to analyze broad ontology preservation. Use `important_subset` to analyze practical conversion fidelity to runnable framework code.

## WGI Interpretation

WGI compares workflow graph topology between KG and generated code. The main `score` uses the better of labeled graph matching and unlabeled topology matching. Labeled missing/extra edges are still reported for debugging.
