from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS


def parse_kg(file_path: str):
    # Namespaces
    AGENTO = Namespace("http://www.w3id.org/agentic-ai/onto#")
    DCT = DCTERMS

    # Load RDF Graph
    g = Graph()
    try:
        g.parse(file_path, format="turtle")
    except Exception as e:
        # Coba dengan format lain jika turtle gagal
        try:
            g.parse(file_path, format="xml")
        except:
            # Jika masih gagal, lempar error dengan pesan yang jelas
            raise ValueError(f"Failed to parse RDF file. Please check TTL syntax in {file_path}. Error: {str(e)}")

    parsed = {
        "agents": [],
        "tasks": [],
        "tools": [],
        "goals": [],
        "workflows": [],
    }

    # Parse Agents
    for agent in g.subjects(RDF.type, AGENTO.Agent):
        role = g.value(agent, AGENTO.agentRole) or g.value(agent, DCT.title)
        goal = g.value(agent, AGENTO.hasGoal)
        goal_label = None
        if goal:
            goal_label = g.value(goal, DCT.title) or g.value(goal, DCT.description)

        tasks = [str(o) for o in g.objects(agent, AGENTO.hasTask)]
        tools = [str(o) for o in g.objects(agent, AGENTO.usesTool)]

        parsed["agents"].append({
            "id": str(agent),
            "role": str(role) if role else "",
            "goal": str(goal_label) if goal_label else "",
            "tasks": tasks,
            "tools": tools
        })

    # Parse Tasks
    for task in g.subjects(RDF.type, AGENTO.Task):
        desc = g.value(task, DCT.description)
        expected = g.value(task, AGENTO.taskExpectedOutput)
        parsed["tasks"].append({
            "id": str(task),
            "description": str(desc) if desc else "",
            "expected_output": str(expected) if expected else ""
        })

    # Parse Tools
    for tool in g.subjects(RDF.type, AGENTO.Tool):
        desc = g.value(tool, DCT.description)
        resource = g.value(tool, AGENTO.accessesResource)
        parsed["tools"].append({
            "id": str(tool),
            "description": str(desc) if desc else "",
            "resource": str(resource) if resource else ""
        })

    # Parse Goals
    for goal in g.subjects(RDF.type, AGENTO.Goal):
        title = g.value(goal, DCT.title)
        desc = g.value(goal, DCT.description)
        parsed["goals"].append({
            "id": str(goal),
            "title": str(title) if title else "",
            "description": str(desc) if desc else ""
        })

    # Parse WorkflowPatterns & Steps
    for wf in g.subjects(RDF.type, AGENTO.WorkflowPattern):
        steps = [str(o) for o in g.objects(wf, AGENTO.hasWorkflowStep)]
        pattern_type = g.value(wf, DCT.title) or "WorkflowPattern"
        parsed["workflows"].append({
            "id": str(wf),
            "type": str(pattern_type),
            "steps": steps
        })

    print(f"[INFO] Parsed {len(parsed['agents'])} agents, "
          f"{len(parsed['tasks'])} tasks, {len(parsed['tools'])} tools, "
          f"{len(parsed['workflows'])} workflows.")

    return parsed


# Quick test
if __name__ == "__main__":
    example_path = "kg_g3/crewai/email_auto_responder_flow.rdf"
    try:
        result = parse_kg(example_path)
        print("\n=== Agents ===")
        for a in result["agents"]:
            print(a)
        print("\n=== Tasks ===")
        for t in result["tasks"]:
            print(t)
    except FileNotFoundError:
        print("[ERROR] RDF file not found. Check rdf/ directory.")