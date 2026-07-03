import asyncio

from team import (
    agent_id_constructor_parameter,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution
        # ==================================================
        # Workflow Step: task_get_agent_card
        # Workflow Edge: task_get_agent_card -> task_send_message
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_get_agent_card")
        print("=" * 80)

        task_prompt = """Retrieve agent card metadata (getAgentCard / getExtendedAgentCard). """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_send_message
        # Workflow Edge: task_send_message -> task_send_message_stream
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_send_message")
        print("=" * 80)

        task_prompt = """Send a single message to an agent and receive a message or task response. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_send_message_stream
        # Workflow Edge: task_send_message_stream -> task_get_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_send_message_stream")
        print("=" * 80)

        task_prompt = """Initiate a streaming message to receive real-time task events. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_get_task
        # Workflow Edge: task_get_task -> task_cancel_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_get_task")
        print("=" * 80)

        task_prompt = """Query status and result of an existing task. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_cancel_task
        # Workflow Edge: task_cancel_task -> task_resubscribe_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_cancel_task")
        print("=" * 80)

        task_prompt = """Cancel a running task for the agent. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_resubscribe_task
        # Workflow Edge: task_resubscribe_task -> task_set_push_notification_config
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_resubscribe_task")
        print("=" * 80)

        task_prompt = """Resume a previously started task stream to receive ongoing updates. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_set_push_notification_config
        # Workflow Edge: task_set_push_notification_config -> task_get_push_notification_config
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_set_push_notification_config")
        print("=" * 80)

        task_prompt = """Set push notification configuration for a task. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_get_push_notification_config
        # Workflow Edge: task_get_push_notification_config -> task_list_push_notification_config
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_get_push_notification_config")
        print("=" * 80)

        task_prompt = """Get push notification configuration for a task. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_list_push_notification_config
        # Workflow Edge: task_list_push_notification_config -> task_delete_push_notification_config
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_list_push_notification_config")
        print("=" * 80)

        task_prompt = """List push notification configurations. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_delete_push_notification_config
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_delete_push_notification_config")
        print("=" * 80)

        task_prompt = """Delete a push notification configuration for a task. """
        # Execute via the assigned agent: agent_id_constructor_parameter
        result = await agent_id_constructor_parameter.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        print("\n" + "=" * 80)
        print("DONE")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)
        print(type(e).__name__)
        print(str(e))



if __name__ == "__main__":
    asyncio.run(main())