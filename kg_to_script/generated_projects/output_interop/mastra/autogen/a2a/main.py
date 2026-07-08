import asyncio

from team import (
    agent_id_constructor_parameter,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)
from autogen_agentchat.messages import BaseChatMessage, TextMessage

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution.
        #
        # `history` accumulates every step's real conversation so far and is
        # threaded into each subsequent step's .run() call. Without this,
        # each step only ever sees its own task prompt in isolation - later
        # steps (e.g. "review the draft") have no way to see what an earlier
        # step (e.g. "draft the posting") actually produced.
        history: list[BaseChatMessage] = []
        # ==================================================
        # Workflow Step: task_get_agent_card
        # Workflow Edge: task_get_agent_card -> task_send_message
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_get_agent_card")
        print("=" * 80)

        task_prompt = """Request agent card metadata via GET /.well-known/{agentId}/agent-card.json or via JSON-RPC agent/getAuthenticatedExtendedCard. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Send a message to the agent using JSON-RPC method message/send with MessageSendParams. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Open a message/stream JSON-RPC request (SSE) to receive incremental A2A events for the initiated message/task. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/get JSON-RPC with TaskQueryParams to retrieve task status and result. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/cancel JSON-RPC with TaskQueryParams to cancel a running task. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/resubscribe JSON-RPC with TaskIdParams and stream true to reattach to an existing task stream. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/pushNotificationConfig/set JSON-RPC with a TaskPushNotificationConfig object. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/pushNotificationConfig/get JSON-RPC with identifying params. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/pushNotificationConfig/list JSON-RPC to retrieve configurations. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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

        task_prompt = """Call tasks/pushNotificationConfig/delete JSON-RPC with identifying params to delete a config. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent_id_constructor_parameter, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent_id_constructor_parameter.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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