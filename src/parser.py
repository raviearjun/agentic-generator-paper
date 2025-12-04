from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS


def parse_kg(file_path: str):
    """
    Parse Knowledge Graph file (TTL/RDF) and extract ALL AgentO components.
    Translates KG AS-IS - if KG is incomplete, output will be incomplete.
    """
    # Namespaces
    AGENTO = Namespace("http://www.w3id.org/agentic-ai/onto#")
    DCT = DCTERMS

    # Load RDF Graph
    g = Graph()
    try:
        g.parse(file_path, format="turtle")
    except Exception as e:
        try:
            g.parse(file_path, format="xml")
        except:
            raise ValueError(f"Failed to parse RDF file. Please check TTL syntax in {file_path}. Error: {str(e)}")

    parsed = {
        "agents": [],
        "tasks": [],
        "tools": [],
        "goals": [],
        "workflows": [],
        "workflow_steps": [],
        "agent_interactions": [],  # NEW: untuk interactsWith
    }

    # Build reverse mapping: Task ID -> Agent ID (dari hasTask)
    task_to_agent = {}
    for agent in g.subjects(RDF.type, AGENTO.Agent):
        for task in g.objects(agent, AGENTO.hasTask):
            task_to_agent[str(task)] = str(agent)

    # Parse Agents dengan semua properti dari KG
    for agent in g.subjects(RDF.type, AGENTO.Agent):
        agent_id = str(agent)
        
        # Basic properties
        role = g.value(agent, AGENTO.agentRole)
        agent_id_prop = g.value(agent, AGENTO.agentID)
        title = g.value(agent, DCT.title)
        description = g.value(agent, DCT.description)
        
        # Goal reference
        goal_ref = g.value(agent, AGENTO.hasGoal)
        goal_label = None
        goal_desc = None
        if goal_ref:
            goal_label = g.value(goal_ref, DCT.title)
            goal_desc = g.value(goal_ref, DCT.description)
        
        # Related entities
        tasks = [str(o) for o in g.objects(agent, AGENTO.hasTask)]
        tools = [str(o) for o in g.objects(agent, AGENTO.usesTool)]
        interacts_with = [str(o) for o in g.objects(agent, AGENTO.interactsWith)]
        
        parsed["agents"].append({
            "id": agent_id,
            "agent_id_prop": str(agent_id_prop) if agent_id_prop else "",
            "role": str(role) if role else "",
            "title": str(title) if title else "",
            "description": str(description) if description else "",
            "goal_title": str(goal_label) if goal_label else "",
            "goal_description": str(goal_desc) if goal_desc else "",
            "tasks": tasks,
            "tools": tools,
            "interacts_with": interacts_with,
        })
        
        # Track interactions
        for target in interacts_with:
            parsed["agent_interactions"].append({
                "from": agent_id,
                "to": target
            })

    # Parse Tasks dengan agent assignment dari KG
    for task in g.subjects(RDF.type, AGENTO.Task):
        task_id = str(task)
        title = g.value(task, DCT.title)
        desc = g.value(task, DCT.description)
        expected = g.value(task, AGENTO.taskExpectedOutput)
        
        # Get agent yang memiliki task ini (reverse lookup dari hasTask)
        assigned_agent = task_to_agent.get(task_id, "")
        
        parsed["tasks"].append({
            "id": task_id,
            "title": str(title) if title else "",
            "description": str(desc) if desc else "",
            "expected_output": str(expected) if expected else "",
            "assigned_agent": assigned_agent,  # NEW: dari relasi hasTask
        })

    # Parse Tools
    for tool in g.subjects(RDF.type, AGENTO.Tool):
        title = g.value(tool, DCT.title)
        desc = g.value(tool, DCT.description)
        resource = g.value(tool, AGENTO.accessesResource)
        parsed["tools"].append({
            "id": str(tool),
            "title": str(title) if title else "",
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

    # Parse WorkflowPatterns
    for wf in g.subjects(RDF.type, AGENTO.WorkflowPattern):
        title = g.value(wf, DCT.title)
        desc = g.value(wf, DCT.description)
        steps = [str(o) for o in g.objects(wf, AGENTO.hasWorkflowStep)]
        
        parsed["workflows"].append({
            "id": str(wf),
            "title": str(title) if title else "",
            "description": str(desc) if desc else "",
            "steps": steps
        })

    # Parse WorkflowSteps
    for step in g.subjects(RDF.type, AGENTO.WorkflowStep):
        title = g.value(step, DCT.title)
        performed_by = g.value(step, AGENTO.performedBy)
        next_step = g.value(step, AGENTO.nextStep)
        step_order = g.value(step, AGENTO.stepOrder)
        associated_task = g.value(step, AGENTO.hasAssociatedTask)
        
        parsed["workflow_steps"].append({
            "id": str(step),
            "title": str(title) if title else "",
            "performed_by": str(performed_by) if performed_by else "",
            "next_step": str(next_step) if next_step else "",
            "step_order": int(step_order) if step_order else 0,
            "associated_task": str(associated_task) if associated_task else "",
        })

    print(f"[INFO] Parsed {len(parsed['agents'])} agents, "
          f"{len(parsed['tasks'])} tasks, {len(parsed['tools'])} tools, "
          f"{len(parsed['workflows'])} workflows, {len(parsed['workflow_steps'])} steps, "
          f"{len(parsed['agent_interactions'])} interactions.")

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