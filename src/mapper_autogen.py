from datetime import datetime


def generate_autogen_code(parsed_data: dict) -> str:

    header = f'''"""
Auto-generated AutoGen Script
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-------------------------------------------------------------
Source: Knowledge Graph (AgentO Ontology)
"""

from autogen import AssistantAgent, UserProxyAgent
# Additional imports or tools can be integrated here.
'''

    agents_code = []
    chat_flow = []
    manager_setup = []

    # Generate Assistant Agents
    for agent in parsed_data["agents"]:
        agent_name = agent["id"].split("#")[-1]
        agent_var = agent_name.lower()
        role = agent["role"] or "Unnamed Agent"
        goal = agent["goal"] or "Undefined goal"
        desc = f"{role} is part of an automatically generated AutoGen workflow."

        code = f"""
# {role} 
{agent_var} = AssistantAgent(
    name="{agent_name}",
    system_message=\"\"\"You are {role}. {desc}
Your main goal: {goal}.\"\"\"
)
"""
        agents_code.append(code)

    # Define Conversation Flow 
    chat_flow.append("""
# Define Manager (User Proxy)
manager = UserProxyAgent(name="manager")

# Conversation Flow 
print("Starting AutoGen conversation workflow...")
""")

    # If there’s a WorkflowPattern, generate sequential chat order
    if parsed_data["workflows"]:
        steps = parsed_data["workflows"][0]["steps"]
        ordered_agents = []
        for step in steps:
            # Find which agent performs this step
            step_agent = None
            for agent in parsed_data["agents"]:
                if any(step_task in agent["tasks"] for step_task in parsed_data["tasks"]):
                    step_agent = agent["id"].split("#")[-1].lower()
                    break
            if not step_agent:
                step_agent = parsed_data["agents"][0]["id"].split("#")[-1].lower()
            ordered_agents.append(step_agent)

        for i in range(len(ordered_agents) - 1):
            sender = ordered_agents[i]
            receiver = ordered_agents[i + 1]
            chat_flow.append(
                f'manager.initiate_chat({sender}, message="Proceed with your step.")\n'
                f'{sender}.initiate_chat({receiver}, message="Task completed. Continue next step.")\n'
            )
    else:
        # Default case if no workflow data available
        if len(parsed_data["agents"]) >= 2:
            a1 = parsed_data["agents"][0]["id"].split("#")[-1].lower()
            a2 = parsed_data["agents"][1]["id"].split("#")[-1].lower()
            chat_flow.append(
                f'manager.initiate_chat({a1}, message="Start your assigned task.")\n'
                f'{a1}.initiate_chat({a2}, message="Passing results for summarization.")\n'
            )
        else:
            a1 = parsed_data["agents"][0]["id"].split("#")[-1].lower()
            chat_flow.append(f'manager.initiate_chat({a1}, message="Begin your assigned task.")\n')

    # Combine all sections
    final_script = header + "\n".join(agents_code) + "\n".join(chat_flow)

    return final_script


# Quick test 
if __name__ == "__main__":
    from parser import parse_kg
    parsed = parse_kg("kg_g3/autogen/chess_game.rdf")

    code = generate_autogen_code(parsed)

    # Write to file
    with open("output/autogen_generated.py", "w") as f:
        f.write(code)

    print("[INFO] AutoGen code generated → output/autogen_generated.py")