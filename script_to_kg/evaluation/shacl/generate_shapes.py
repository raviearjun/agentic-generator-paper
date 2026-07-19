#!/usr/bin/env python3
"""
generate_shapes.py

Generates core.shapes.ttl: SHACL shapes derived directly from the Agentic AI
Ontology (../../../agentO.ttl) — class-level domain/range typing for object
properties (sh:class), XSD datatypes for data properties (sh:datatype), and
basic "should have" cardinality on identity/scalar fields. Pure SHACL Core
(no SPARQL-based constraints/targets, no dependency on evaluate_kgs.py) —
validates ontology-structural conformance only, not framework- or
project-specific expected coverage.

Re-run this script whenever agentO.ttl changes, to regenerate core.shapes.ttl.
"""

from pathlib import Path
from rdflib import Graph, Namespace, Literal, BNode, RDF, RDFS, XSD, OWL

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

AGENTO = Namespace("http://www.w3id.org/agentic-ai/onto#")
BEAM = Namespace("http://w3id.org/beam/core#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")

SHAPES_NS = Namespace("http://www.w3id.org/agentic-ai/shacl#")

# ─────────────────────────────────────────────────────────────────────────
# Ontology-derived facts (mirrors agentO.ttl; kept explicit/readable rather
# than re-deriving owl:unionOf domains programmatically, since the ontology
# is small and static).
# ─────────────────────────────────────────────────────────────────────────

# object property -> (domain class local name or None, range class local name or beam/prov IRI)
OBJECT_PROPS = {
    "agentPrompt":           ("LLMAgent", AGENTO.Prompt),
    "agentResourceUsage":    ("LLMAgent", BEAM.Resource),
    "agentToolUsage":        ("LLMAgent", AGENTO.Tool),
    "containsResource":      ("Environment", BEAM.Resource),
    "contributesToGoal":     ("Objective", AGENTO.Goal),
    "contributesToObjective":("Task", AGENTO.Objective),
    "hasAgentCapability":    ("LLMAgent", AGENTO.Capability),
    "hasAgentConfig":        ("LLMAgent", AGENTO.Config),
    "hasAgentGoal":          ("LLMAgent", AGENTO.Goal),
    "hasAgentMember":        ("Team", AGENTO.LLMAgent),
    "hasAssociatedTask":     ("WorkflowStep", AGENTO.Task),
    "hasCapability":         ("Tool", AGENTO.Capability),
    "hasEnvironmentConfig":  ("Environment", AGENTO.Config),
    "hasKnowledge":          ("LLMAgent", AGENTO.KnowledgeBase),
    "hasRelatedPattern":     ("WorkflowPattern", AGENTO.WorkflowPattern),
    "hasSubPattern":         ("WorkflowPattern", AGENTO.WorkflowPattern),
    "hasSystemConfig":       ("Team", AGENTO.Config),
    "hasTeamGoal":           ("Team", AGENTO.Goal),
    "hasToolConfig":         ("Tool", AGENTO.Config),
    "hasWorkflowPattern":    ("Team", AGENTO.WorkflowPattern),
    "hasWorkflowStep":       ("WorkflowPattern", AGENTO.WorkflowStep),
    "humanParticipatedIn":   ("HumanAgent", AGENTO.Task),
    "interactsWith":         ("LLMAgent", AGENTO.LLMAgent),
    "nextPattern":           ("WorkflowPattern", AGENTO.WorkflowPattern),
    "nextStep":              ("WorkflowStep", AGENTO.WorkflowStep),
    "operatesIn":            ("LLMAgent", AGENTO.Environment),
    "performedBy":           ("Task", AGENTO.Tool),
    "performedByAgent":      ("Task", AGENTO.LLMAgent),
    "producedResource":      ("Task", BEAM.Resource),
    "relatedStep":           ("WorkflowStep", AGENTO.WorkflowStep),
    "requiresCapability":    ("Task", AGENTO.Capability),
    "requiresResource":      ("Task", BEAM.Resource),
    "resourceUsage":         ("Tool", BEAM.Resource),
    "taskPrompt":            ("Task", AGENTO.Prompt),
    "toolUsage":             ("Tool", AGENTO.Tool),
    "useLanguageModel":      ("LLMAgent", AGENTO.LanguageModel),
    # abstract/union-domain properties: real KGs consistently use the more
    # specific sub-properties above (hasAgentGoal/hasTeamGoal, agentPrompt/
    # taskPrompt, ...), so these are modelled loosely (no domain restriction).
    "hasConfig":             (None, AGENTO.Config),
    "hasGoal":               (None, AGENTO.Goal),
    "hasObjective":          (None, AGENTO.Objective),
    "hasPrompt":             (None, AGENTO.Prompt),
}

# data property -> (domain class local name or None, xsd datatype)
DATA_PROPS = {
    "agentID":               ("LLMAgent", XSD.string),
    "agentRole":              ("LLMAgent", XSD.string),
    "configKey":              ("Config", XSD.string),
    "configValue":            ("Config", XSD.string),
    "envType":                ("Environment", XSD.string),
    "promptContext":          ("Prompt", XSD.string),
    "promptInputData":        ("Prompt", XSD.string),
    "promptInstruction":      ("Prompt", XSD.string),
    "promptOutputIndicator":  ("Prompt", XSD.string),
    "stepOrder":              ("WorkflowStep", XSD.integer),
}

# Properties considered "should have exactly one value" (identity/scalar
# fields) vs. properties that are naturally multi-valued relations.
FUNCTIONAL_PROPS = {
    "agentID", "agentRole", "configKey", "configValue", "stepOrder",
}

# Structural "should have at least one" expectations per class, independent
# of framework (soft — emitted with sh:severity sh:Warning, not sh:Violation,
# since not every legitimate KG uses every relation). Each entry verified
# against actual per-project coverage across generated_kgs/ (not just
# pooled per-individual counts, which can hide a gap that's concentrated in
# one outlier file rather than genuinely spread across projects). A rule is
# only kept if EVERY project containing at least one individual of the class
# has 100% coverage of the property — i.e. zero files with any gap:
#   LLMAgent.agentID 41/41 files 100% compliant, .agentRole 41/41,
#     .useLanguageModel 41/41
#   WorkflowStep.stepOrder 40/40 files 100% compliant
#   Config.configKey 36/36 files 100%, .configValue 36/36
#   Team.hasWorkflowPattern 39/39 files 100%
#   WorkflowPattern.hasWorkflowStep 41/41 files 100%
# Dropped despite looking like a majority pattern in pooled per-individual
# counts, because the gap turned out to be concentrated in exactly one
# project rather than spread across many (not a universal "should have"):
#   Task.taskPrompt — 40/41 files 100% compliant; the 1 non-compliant file
#     (dane) alone accounts for all pooled misses (19/191 individuals)
#   Team.hasAgentMember — 38/39 files 100% compliant; the 1 non-compliant
#     file (workflow-with-inline-steps) is the sole miss
#   Tool.hasToolConfig — pooled coverage only 66% (63/95); most Tools
#     genuinely need no config/API key, not a "should have" pattern at all
RECOMMENDED_MIN1 = {
    "LLMAgent": ["agentID", "agentRole", "useLanguageModel"],
    "WorkflowStep": ["stepOrder"],
    "Config": ["configKey", "configValue"],
    "Team": ["hasWorkflowPattern"],
    "WorkflowPattern": ["hasWorkflowStep"],
}

# Class hierarchy (subset relevant to instance data), for reference comments.
SUBCLASS_OF = {
    "Constraint": "KnowledgeBase",
    "EndStep": "WorkflowStep",
    "Environment": "Context",
    "Goal": "Context",
    "HumanAgent": "prov:Agent",
    "KnowledgeBase": "Instance",
    "LLMAgent": "prov:Agent, Tool",
    "LanguageModel": "beam:StatisticalModel",
    "Memory": "KnowledgeBase",
    "Objective": "Context",
    "StartStep": "WorkflowStep",
    "Team": "beam:System",
    "WorkflowPattern": "p-plan:Plan",
    "WorkflowStep": "p-plan:Step",
}

ALL_CLASSES = [
    "Capability", "Config", "Constraint", "Context", "EndStep", "Environment",
    "Goal", "HumanAgent", "Instance", "KnowledgeBase", "LLMAgent",
    "LanguageModel", "Memory", "Objective", "Prompt", "StartStep", "Task",
    "Team", "Tool", "WorkflowPattern", "WorkflowStep",
]

CORE_SHAPES_FILENAME = "core.shapes.ttl"


def new_shapes_graph():
    g = Graph()
    g.bind("sh", SH)
    g.bind("agento", AGENTO)
    g.bind("beam", BEAM)
    g.bind("dcterms", DCTERMS)
    g.bind("prov", PROV)
    g.bind("owl", OWL)
    g.bind("xsd", XSD)
    g.bind("", SHAPES_NS)
    return g


def add_property_shape(g, node_shape, path, *, sh_class=None, datatype=None,
                        min_count=None, max_count=None, message=None,
                        severity=None):
    bn = BNode()
    g.add((node_shape, SH.property, bn))
    g.add((bn, SH.path, path))
    if sh_class is not None:
        g.add((bn, SH['class'], sh_class))
    if datatype is not None:
        g.add((bn, SH.datatype, datatype))
    if min_count is not None:
        g.add((bn, SH.minCount, Literal(min_count)))
    if max_count is not None:
        g.add((bn, SH.maxCount, Literal(max_count)))
    if message is not None:
        g.add((bn, SH.message, Literal(message, lang="en")))
    if severity is not None:
        g.add((bn, SH.severity, severity))
    return bn


def build_core_shapes():
    g = new_shapes_graph()

    ontology_node = SHAPES_NS["core"]
    g.add((ontology_node, RDF.type, OWL.Ontology))
    g.add((ontology_node, RDFS.label,
            Literal("Agentic AI Ontology - Core SHACL Shapes", lang="en")))
    g.add((ontology_node, RDFS.comment, Literal(
        "Structural SHACL shapes derived from agentO.ttl: class-level "
        "domain/range typing for object properties, XSD datatypes for data "
        "properties, and basic 'should have' cardinality. Self-contained "
        "SHACL Core only — no framework/project-specific coverage checks, "
        "no SPARQL-based constraints.", lang="en")))

    # group properties by domain class
    by_domain_obj = {}
    for prop, (domain, rng) in OBJECT_PROPS.items():
        by_domain_obj.setdefault(domain, []).append((prop, rng))

    by_domain_data = {}
    for prop, (domain, dt) in DATA_PROPS.items():
        by_domain_data.setdefault(domain, []).append((prop, dt))

    for cls in ALL_CLASSES:
        obj_props = by_domain_obj.get(cls, [])
        data_props = by_domain_data.get(cls, [])
        if not obj_props and not data_props:
            continue

        shape = SHAPES_NS[f"{cls}Shape"]
        g.add((shape, RDF.type, SH.NodeShape))
        g.add((shape, SH.targetClass, AGENTO[cls]))
        g.add((shape, RDFS.label, Literal(f"{cls} shape", lang="en")))
        if cls in SUBCLASS_OF:
            g.add((shape, RDFS.comment, Literal(
                f"{cls} rdfs:subClassOf {SUBCLASS_OF[cls]} in agentO.ttl.",
                lang="en")))

        recommended = set(RECOMMENDED_MIN1.get(cls, []))

        for prop, rng in obj_props:
            min_count = 1 if prop in recommended else None
            max_count = 1 if prop in FUNCTIONAL_PROPS else None
            add_property_shape(
                g, shape, AGENTO[prop],
                sh_class=rng,
                min_count=min_count,
                max_count=max_count,
                severity=SH.Warning if min_count else SH.Violation,
                message=(
                    f"{cls} should have at least one :{prop} (range :{rng.split('#')[-1] if '#' in str(rng) else rng})."
                    if min_count else
                    f"Value of :{prop} on a :{cls} must be of type {g.namespace_manager.normalizeUri(rng)}."
                ),
            )

        for prop, dt in data_props:
            min_count = 1 if prop in recommended else None
            max_count = 1 if prop in FUNCTIONAL_PROPS else None
            add_property_shape(
                g, shape, AGENTO[prop],
                datatype=dt,
                min_count=min_count,
                max_count=max_count,
                severity=SH.Warning if min_count else SH.Violation,
                message=(
                    f"{cls} should have a :{prop} value."
                    if min_count else
                    f"Value of :{prop} on a :{cls} must be a {g.namespace_manager.normalizeUri(dt)}."
                ),
            )

    # dcterms:title / description / reference: loose, any class, datatype-only,
    # maxCount 1 for title (a resource has one name).
    title_shape = SHAPES_NS["DctermsTitleShape"]
    g.add((title_shape, RDF.type, SH.NodeShape))
    g.add((title_shape, SH.targetSubjectsOf, DCTERMS.title))
    add_property_shape(g, title_shape, DCTERMS.title, datatype=XSD.string,
                        max_count=1, severity=SH.Violation,
                        message="dcterms:title must be a single xsd:string.")

    desc_shape = SHAPES_NS["DctermsDescriptionShape"]
    g.add((desc_shape, RDF.type, SH.NodeShape))
    g.add((desc_shape, SH.targetSubjectsOf, DCTERMS.description))
    add_property_shape(g, desc_shape, DCTERMS.description, datatype=XSD.string,
                        severity=SH.Violation,
                        message="dcterms:description must be an xsd:string.")

    ref_shape = SHAPES_NS["DctermsReferenceShape"]
    g.add((ref_shape, RDF.type, SH.NodeShape))
    g.add((ref_shape, SH.targetSubjectsOf, DCTERMS.reference))
    add_property_shape(g, ref_shape, DCTERMS.reference, datatype=XSD.string,
                        severity=SH.Violation,
                        message="dcterms:reference must be an xsd:string.")

    return g


def serialize(g: Graph, path: Path):
    text = g.serialize(format="turtle")
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO)} ({len(g)} triples)")


def main():
    core_g = build_core_shapes()
    serialize(core_g, HERE / CORE_SHAPES_FILENAME)


if __name__ == "__main__":
    main()
