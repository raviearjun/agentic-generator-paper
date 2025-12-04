from datetime import datetime


def generate_autogen_code(parsed_data: dict) -> str:
    """
    Generate AutoGen code from parsed KG data.
    Translates KG AS-IS:
    - Uses interactsWith relationship for conversation flow
    - Uses workflow_steps for sequential execution order
    - If KG missing these, generates minimal/broken code (KG's fault)
    """

    header = f'''"""
Auto-generated AutoGen Script
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-------------------------------------------------------------
Source: Knowledge Graph (AgentO Ontology)

NOTE: This code is generated AS-IS from the Knowledge Graph.
If conversation flow is missing or incorrect, it indicates
the source KG is incomplete (missing interactsWith or WorkflowStep), 
not a pipeline error.
"""

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import os

# LLM Configuration - user must provide API key
llm_config = {{
    "config_list": [
        {{
            "model": "gpt-4",
            "api_key": os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
        }}
    ]
}}

'''

    agents_code = []
    agent_vars = []
    agent_var_map = {}  # id -> variable name
    
    # Track which agents interact with others (from KG's interactsWith)
    agent_interactions = {}  # agent_var -> [list of agents they interact with]

    # Generate Agents - translate ALL properties from KG
    for agent in parsed_data["agents"]:
        agent_name = agent["id"].split("#")[-1]
        agent_var = agent_name.lower()
        agent_var_map[agent["id"]] = agent_var
        agent_vars.append(agent_var)
        
        # Use KG values as-is
        role = agent.get("role", "")
        goal = agent.get("goal_title", "") or agent.get("goal_description", "")
        desc = agent.get("description", "")
        
        # Build interaction list from KG's interactsWith
        interacts_with = agent.get("interacts_with", [])
        interact_vars = []
        for interact_id in interacts_with:
            interact_var = interact_id.split("#")[-1].lower()
            interact_vars.append(interact_var)
        if interact_vars:
            agent_interactions[agent_var] = interact_vars
        
        # Generate agent code with KG values
        system_msg = f"You are {role}." if role else f"You are agent {agent_name}."
        if goal:
            system_msg += f" Your goal: {goal}."
        if desc:
            system_msg += f" {desc}"

        code = f'''
# Agent: {agent_var}
# Role from KG: {repr(role)}
# Goal from KG: {repr(goal)}
# Interacts with: {interact_vars if interact_vars else "NOT_SPECIFIED_IN_KG"}
{agent_var} = AssistantAgent(
    name="{agent_name}",
    system_message="""{system_msg}""",
    llm_config=llm_config
)
'''
        agents_code.append(code)

    # Generate UserProxyAgent (manager)
    manager_code = '''
# User Proxy Agent (manages conversation)
manager = UserProxyAgent(
    name="manager",
    human_input_mode="NEVER",  # Set to "ALWAYS" for human-in-loop
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "workspace", "use_docker": False}
)
'''

    # Generate Conversation Flow - based on KG relationships
    chat_flow_code = []
    
    # Try workflow_steps first (most explicit)
    workflow_steps = parsed_data.get("workflow_steps", [])
    if workflow_steps:
        # Use workflow steps for conversation order
        chat_flow_code.append('''
# Conversation Flow (from KG WorkflowSteps)
# Executing steps in order defined by stepOrder/nextStep''')
        
        # Sort by step order
        sorted_steps = sorted(workflow_steps, key=lambda s: s.get("step_order", 0))
        
        prev_agent_var = None
        for step in sorted_steps:
            performed_by = step.get("performed_by", "")
            step_name = step.get("id", "").split("#")[-1]
            
            if performed_by:
                agent_var = performed_by.split("#")[-1].lower()
                
                if prev_agent_var is None:
                    # First step - manager initiates
                    chat_flow_code.append(f'''
    # Step: {step_name}
    manager.initiate_chat({agent_var}, message="Please begin your assigned task.")''')
                else:
                    # Subsequent steps - agent to agent
                    chat_flow_code.append(f'''
    # Step: {step_name}
    # {prev_agent_var} -> {agent_var}
    {prev_agent_var}.initiate_chat({agent_var}, message="I have completed my part. Please proceed with your task.")''')
                
                prev_agent_var = agent_var
            else:
                chat_flow_code.append(f'''
    # Step: {step_name} - WARNING: No performedBy in KG (cannot determine agent)''')
    
    elif agent_interactions:
        # Use interactsWith relationships
        chat_flow_code.append('''
# Conversation Flow (from KG interactsWith relationships)''')
        
        # Start with first agent
        if agent_vars:
            first_agent = agent_vars[0]
            chat_flow_code.append(f'''
    manager.initiate_chat({first_agent}, message="Please begin your assigned task.")''')
            
            # Follow interaction chain
            visited = set([first_agent])
            current = first_agent
            while current in agent_interactions:
                next_agents = agent_interactions[current]
                for next_agent in next_agents:
                    if next_agent not in visited and next_agent in agent_vars:
                        chat_flow_code.append(f'''
    {current}.initiate_chat({next_agent}, message="I have completed my part. Please proceed.")''')
                        visited.add(next_agent)
                        current = next_agent
                        break
                else:
                    break
    
    elif len(agent_vars) >= 2:
        # Fallback: no workflow steps or interactions in KG - use simple order
        chat_flow_code.append('''
# Conversation Flow (FALLBACK - KG missing WorkflowSteps and interactsWith)
# WARNING: Using agent definition order as KG does not specify interaction pattern''')
        
        chat_flow_code.append(f'''
    manager.initiate_chat({agent_vars[0]}, message="Please begin your assigned task.")''')
        for i in range(len(agent_vars) - 1):
            chat_flow_code.append(f'''
    {agent_vars[i]}.initiate_chat({agent_vars[i+1]}, message="Passing to next agent.")''')
    
    elif len(agent_vars) == 1:
        # Single agent
        chat_flow_code.append(f'''
# Single agent workflow
    manager.initiate_chat({agent_vars[0]}, message="Please complete your assigned task.")''')
    
    else:
        # No agents!
        chat_flow_code.append('''
# ERROR: No agents found in KG
# Cannot generate conversation flow without agents''')

    # Main block
    if agent_vars:
        main_block = f'''
# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    print("Starting AutoGen conversation workflow...")
    print(f"Agents from KG: {len(agent_vars)}")
    print("Agent interactions from KG: {len(agent_interactions)}")
    print("Workflow steps from KG: {len(workflow_steps)}")
    print("-" * 50)
    
{"".join(chat_flow_code)}
    
    print("-" * 50)
    print("Workflow completed.")
'''
    else:
        main_block = '''
# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    print("ERROR: No agents defined in source Knowledge Graph")
    print("Please ensure KG contains instances of type agento:Agent")
'''

    # Combine all sections
    final_script = header
    final_script += "# ========== AGENTS ==========\n"
    final_script += "\n".join(agents_code) if agents_code else "# No agents found in KG\n"
    final_script += "\n" + manager_code
    final_script += main_block

    return final_script


# Quick test 
if __name__ == "__main__":
    from parser import parse_kg
    parsed = parse_kg("kg_g3/autogen/chess_game.ttl")

    code = generate_autogen_code(parsed)

    # Write to file
    with open("output/autogen_generated.py", "w", encoding="utf-8") as f:
        f.write(code)

    print("[INFO] AutoGen code generated → output/autogen_generated.py")
