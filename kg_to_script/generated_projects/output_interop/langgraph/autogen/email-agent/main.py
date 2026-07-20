import asyncio

from team import (
    email_assistant_agent,
    human_user,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)
from autogen_agentchat.messages import BaseChatMessage, TextMessage

INPUTS = {
    "CONVERSATION": "Write an email to Alex (alex@example.com) letting them know the product launch has been moved from June 10 to June 24, and ask them to update the marketing calendar accordingly.",
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
        # Workflow Step: task_write_email
        # Workflow Edge: task_write_email -> task_write_email
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_write_email")
        print("=" * 80)

        task_prompt = """You're an AI email assistant, tasked with writing an email for the user.
Use the entire conversation history between you, and the user to craft the email for them.

<conversation>
{CONVERSATION}
</conversation>

If there is NOT enough information to send an email, respond to the user requesting the missing information.
Required fields:
- subject - The subject of the email
- body - The body of the email
- to - The recipient of the email """
        task_prompt = task_prompt.format(**INPUTS)
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: email_assistant_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await email_assistant_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_interrupt
        # Workflow Edge: task_interrupt -> task_send_email
        # Workflow Edge: task_interrupt -> task_rewrite_email
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_interrupt")
        print("=" * 80)

        task_prompt = """# New Email

## Subject
{subject}

## To
{to}

## Body
{body}

## Response Instructions

- **Response**: Any response submitted will be passed to an LLM to rewrite the email. It can rewrite the email body, subject, or recipient.

- **Edit or Accept**: Editing/Accepting the email will send the email.

- **Ignore**: Ignoring the email will end the conversation, and the email will not be sent. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_rewrite_email
        # Workflow Edge: task_rewrite_email -> task_interrupt
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_rewrite_email")
        print("=" * 80)

        task_prompt = """You're an AI email assistant, tasked with rewriting an email for the user.
Here is the current state of the email for the user:
<email>
  <subject>
    {SUBJECT}
  </subject>
  <body>
    {BODY}
  </body>
  <to>
    {TO}
  </to>
</email>

Here is the user's response, which should contain some request for changes to the email:
<user-response>
{USER_RESPONSE}
</user-response>

Given that, please rewrite the email. Do NOT modify anything the user does not request to be changed. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: email_assistant_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await email_assistant_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_send_email
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_send_email")
        print("=" * 80)

        task_prompt = """Render a confirmation UI indicating the email was successfully sent. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: email_assistant_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await email_assistant_agent.run(task=history)
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