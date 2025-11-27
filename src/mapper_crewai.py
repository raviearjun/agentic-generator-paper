from datetime import datetime


def generate_crewai_code(parsed_data: dict) -> str:

    header = f'''"""
Auto-generated CrewAI Script
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-------------------------------------------------------------
Source: Knowledge Graph (AgentO Ontology)
"""

from crewai import Agent, Task, Crew
# Import custom tools if available
# from tools.search_tools import SearchTool
'''

    agents_code = []
    tasks_code = []
    crew_setup = []
    crew_agents = []
    crew_tasks = []

    # Generate Agents 
    for agent in parsed_data["agents"]:
        agent_var = agent["id"].split("#")[-1].lower()
        role = agent["role"] or "Unnamed Agent"
        goal = agent["goal"] or "Undefined goal"
        tools = ", ".join([t.split("#")[-1] for t in agent["tools"]]) if agent["tools"] else ""

        code = f"""
# {role} 
{agent_var} = Agent(
    role="{role}",
    goal="{goal}",
    backstory="{role} is part of an automatically generated Agentic AI workflow.",
    tools=[{tools}] if "{tools}" else []
)
"""
        agents_code.append(code)
        crew_agents.append(agent_var)

    # Generate Tasks
    for task in parsed_data["tasks"]:
        task_var = task["id"].split("#")[-1].lower()
        desc = task["description"] or "No description provided."
        expected = task["expected_output"] or "Undefined output."

        code = f"""
# Task: {task_var}
{task_var} = Task(
    description="{desc}",
    expected_output="{expected}"
)
"""
        tasks_code.append(code)
        crew_tasks.append(task_var)

    # Crew Assembly
    crew_name = "auto_generated_crew"
    crew_block = f"""
# Crew Setup 
{crew_name} = Crew(
    agents=[{", ".join(crew_agents)}],
    tasks=[{", ".join(crew_tasks)}]
)

if __name__ == "__main__":
    print("Running auto-generated CrewAI workflow...")
    {crew_name}.kickoff()
"""

    final_script = header + "\n".join(agents_code) + "\n".join(tasks_code) + crew_block

    return final_script


# Quick test
if __name__ == "__main__":
    from parser import parse_kg
    parsed = parse_kg("kg_g3/crewai/email_auto_responder_flow.rdf")

    code = generate_crewai_code(parsed)

    # Write to file
    with open("output/crewai_generated.py", "w") as f:
        f.write(code)

    print("[INFO] CrewAI code generated → output/crewai_generated.py")