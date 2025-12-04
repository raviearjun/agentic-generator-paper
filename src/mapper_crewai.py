from datetime import datetime


def generate_crewai_code(parsed_data: dict) -> str:
    """
    Generate CrewAI code from parsed KG data.
    Translates KG AS-IS:
    - If KG has agent-task relationship (hasTask), it will be mapped to Task(agent=...)
    - If KG is missing this relationship, generated code will be incomplete (KG's fault)
    - If KG has no agents/tasks, output will have empty Crew (KG's fault)
    """

    header = f'''"""
Auto-generated CrewAI Script
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-------------------------------------------------------------
Source: Knowledge Graph (AgentO Ontology)

NOTE: This code is generated AS-IS from the Knowledge Graph.
If any required components are missing (e.g., agent assignment to tasks),
it indicates the source KG is incomplete, not a pipeline error.
"""

from crewai import Agent, Task, Crew
'''

    agents_code = []
    tasks_code = []
    tools_code = []
    crew_agents = []
    crew_tasks = []
    
    # Build agent ID -> variable name mapping
    agent_var_map = {}
    for agent in parsed_data["agents"]:
        agent_var = agent["id"].split("#")[-1].lower()
        agent_var_map[agent["id"]] = agent_var

    # Generate Tools (if any in KG)
    for tool in parsed_data.get("tools", []):
        tool_var = tool["id"].split("#")[-1].lower()
        tool_desc = tool.get("description", "")
        
        code = f'''
# Tool: {tool_var}
# Description: {tool_desc}
# NOTE: Tool implementation must be provided separately
# {tool_var} = YourToolClass()
'''
        tools_code.append(code)

    # Generate Agents - translate ALL properties from KG
    for agent in parsed_data["agents"]:
        agent_var = agent["id"].split("#")[-1].lower()
        
        # Use KG values as-is, empty string if not in KG
        role = agent.get("role", "")
        goal = agent.get("goal_title", "") or agent.get("goal_description", "")
        backstory = agent.get("description", "")
        
        # Tools from KG (usesTool relationship)
        tool_vars = []
        for tool_id in agent.get("tools", []):
            tool_var = tool_id.split("#")[-1].lower()
            tool_vars.append(tool_var)
        tools_str = ", ".join(tool_vars) if tool_vars else ""
        
        # Generate agent code with KG values
        code = f'''
# Agent: {agent_var}
# Role from KG: {repr(role)}
# Goal from KG: {repr(goal)}
{agent_var} = Agent(
    role={repr(role) if role else repr("MISSING_IN_KG")},
    goal={repr(goal) if goal else repr("MISSING_IN_KG")},
    backstory={repr(backstory) if backstory else repr(f"Agent {agent_var} from KG")},
    tools=[{tools_str}] if {repr(tools_str)} else []
)
'''
        agents_code.append(code)
        crew_agents.append(agent_var)

    # Generate Tasks - with agent assignment from KG's hasTask relationship
    for task in parsed_data["tasks"]:
        task_var = task["id"].split("#")[-1].lower()
        
        # Use KG values as-is
        desc = task.get("description", "")
        expected = task.get("expected_output", "")
        
        # Get assigned agent from KG (reverse of hasTask relationship)
        assigned_agent_id = task.get("assigned_agent", "")
        assigned_agent_var = agent_var_map.get(assigned_agent_id, "")
        
        # Generate task code
        if assigned_agent_var:
            # KG has agent-task relationship - generate valid code
            code = f'''
# Task: {task_var}
# Assigned to agent: {assigned_agent_var} (from KG hasTask relationship)
{task_var} = Task(
    description={repr(desc) if desc else repr("MISSING_IN_KG")},
    expected_output={repr(expected) if expected else repr("MISSING_IN_KG")},
    agent={assigned_agent_var}
)
'''
        else:
            # KG MISSING agent-task relationship - generate code with comment
            code = f'''
# Task: {task_var}
# WARNING: No agent assigned in KG (missing hasTask relationship)
# This will cause runtime error - KG is incomplete
{task_var} = Task(
    description={repr(desc) if desc else repr("MISSING_IN_KG")},
    expected_output={repr(expected) if expected else repr("MISSING_IN_KG")}
    # agent=MISSING - KG does not define which agent performs this task
)
'''
        tasks_code.append(code)
        crew_tasks.append(task_var)

    # Crew Assembly
    crew_name = "auto_generated_crew"
    
    if not crew_agents:
        # No agents in KG
        crew_block = f'''
# WARNING: No agents found in KG
# The source Knowledge Graph does not define any Agent instances
# Crew cannot be created without agents

# {crew_name} = Crew(agents=[], tasks=[])  # Would fail - no agents

if __name__ == "__main__":
    print("ERROR: No agents defined in source Knowledge Graph")
    print("Please ensure KG contains instances of type agento:Agent")
'''
    elif not crew_tasks:
        # Agents but no tasks in KG
        crew_block = f'''
# WARNING: No tasks found in KG
# Agents exist but no Task instances in the Knowledge Graph

{crew_name} = Crew(
    agents=[{", ".join(crew_agents)}],
    tasks=[]  # No tasks defined in KG
)

if __name__ == "__main__":
    print("WARNING: No tasks defined in source Knowledge Graph")
    print("Crew has agents but nothing to execute")
    # {crew_name}.kickoff()  # Would have nothing to do
'''
    else:
        # Normal case - both agents and tasks exist
        crew_block = f'''
# Crew Setup
# Agents from KG: {len(crew_agents)}
# Tasks from KG: {len(crew_tasks)}
{crew_name} = Crew(
    agents=[{", ".join(crew_agents)}],
    tasks=[{", ".join(crew_tasks)}]
)

if __name__ == "__main__":
    print("Running auto-generated CrewAI workflow...")
    print(f"Agents: {len(crew_agents)}, Tasks: {len(crew_tasks)}")
    {crew_name}.kickoff()
'''

    # Combine all sections
    final_script = header
    if tools_code:
        final_script += "\n# ========== TOOLS ==========\n" + "\n".join(tools_code)
    if agents_code:
        final_script += "\n# ========== AGENTS ==========\n" + "\n".join(agents_code)
    if tasks_code:
        final_script += "\n# ========== TASKS ==========\n" + "\n".join(tasks_code)
    final_script += "\n# ========== CREW ==========\n" + crew_block

    return final_script


# Quick test
if __name__ == "__main__":
    from parser import parse_kg
    parsed = parse_kg("kg_g3/crewai/email_auto_responder_flow.rdf")

    code = generate_crewai_code(parsed)

    # Write to file
    with open("output/crewai_generated.py", "w", encoding="utf-8") as f:
        f.write(code)

    print("[INFO] CrewAI code generated → output/crewai_generated.py")