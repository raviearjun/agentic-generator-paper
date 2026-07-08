import asyncio

from team import (
    dane,
    dane_commit_message,
    dane_issue_labeler,
    dane_link_checker,
    dane_change_log,
    dane_new_contributor,
    dane_package_publisher,
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
        # Workflow Step: task_changelog_step_a1
        # Workflow Edge: task_changelog_step_a1 -> task_changelog_step_a2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_changelog_step_a1")
        print("=" * 80)

        task_prompt = """Get a git diff and connect to slack; runs git diff via execa """
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
        # Workflow Step: task_changelog_step_a2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_changelog_step_a2")
        print("=" * 80)

        task_prompt = """Time: recent week
Git diff to generate from: (git diff from previous step)
Task:
1. create a structured narrative changelog that highlights key updates and improvements.
2. Include what packages were changed
Structure: Opening, Major Updates, Technical Improvements, Documentation & Examples, Bug Fixes & Infrastructure
Finally send this to the configured slack channel with slack_post_message tool. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_change_log, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_change_log.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_entry_message_input
        # Workflow Edge: task_entry_message_input -> task_entry_message_output
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_entry_message_input")
        print("=" * 80)

        task_prompt = """Prompt user to input a message (inquirer prompt) """
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
        # Workflow Step: task_entry_message_output
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_entry_message_output")
        print("=" * 80)

        task_prompt = """User-supplied message forwarded to Dane agent for response; context includes threadId and resourceId. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_commit_get_diff
        # Workflow Edge: task_commit_get_diff -> task_commit_read_conventional_commit_spec
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_commit_get_diff")
        print("=" * 80)

        task_prompt = """Compute git diff of staged changes via git command """
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
        # Workflow Step: task_commit_read_conventional_commit_spec
        # Workflow Edge: task_commit_read_conventional_commit_spec -> task_commit_generate_message
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_commit_read_conventional_commit_spec")
        print("=" * 80)

        task_prompt = """Read conventional commit spec using fsTool """
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
        # Workflow Step: task_commit_generate_message
        # Workflow Edge: task_commit_generate_message -> task_commit_confirmation
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_commit_generate_message")
        print("=" * 80)

        task_prompt = """Given the git diff, generate a conventional commit message; obey guidelines (start with verb, concise, first line <50 chars, add body if needed). Return commitMessage, generated flag, and guidelines array. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_commit_message, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_commit_message.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_commit_confirmation
        # Workflow Edge: task_commit_confirmation -> task_commit_commit
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_commit_confirmation")
        print("=" * 80)

        task_prompt = """Prompt human user to confirm commit message via inquirer confirm """
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
        # Workflow Step: task_commit_commit
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_commit_commit")
        print("=" * 80)

        task_prompt = """Perform git commit with generated message (execSync git commit) """
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
        # Workflow Step: task_first_get_pull_request
        # Workflow Edge: task_first_get_pull_request -> task_first_message_generator
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_first_get_pull_request")
        print("=" * 80)

        task_prompt = """Retrieve pull request data from GitHub integration and fetch diff """
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
        # Workflow Step: task_first_message_generator
        # Workflow Edge: task_first_message_generator -> task_first_create_message
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_first_message_generator")
        print("=" * 80)

        task_prompt = """Given PR title, body, and diff plus Mastra docs, generate a friendly intro, a checklist (if applicable), and an outro thanking the contributor. Do not summarize code or give code advice. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_new_contributor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_new_contributor.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_first_create_message
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_first_create_message")
        print("=" * 80)

        task_prompt = """Post generated message as GitHub issue comment using github integration """
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
        # Workflow Step: task_issue_get_issue
        # Workflow Edge: task_issue_get_issue -> task_issue_label_issue
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_issue_get_issue")
        print("=" * 80)

        task_prompt = """Retrieve issue and repository labels using GitHub integration """
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
        # Workflow Step: task_issue_label_issue
        # Workflow Edge: task_issue_label_issue -> task_issue_apply_labels
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_issue_label_issue")
        print("=" * 80)

        task_prompt = """Given issue title, body, and available repo labels, propose one or more labels to assign. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_issue_labeler, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_issue_labeler.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_issue_apply_labels
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_issue_apply_labels")
        print("=" * 80)

        task_prompt = """Add labels to GitHub issue using integrations client """
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
        # Workflow Step: task_link_get_broken_links
        # Workflow Edge: task_link_get_broken_links -> task_link_report_broken_links
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_link_get_broken_links")
        print("=" * 80)

        task_prompt = """Run linkinator via shell to collect links; parse JSON output """
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
        # Workflow Step: task_link_report_broken_links
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_link_report_broken_links")
        print("=" * 80)

        task_prompt = """Format the broken links JSON into a human-friendly Slack message and send to the configured channel using slack_post_message tool. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_link_checker, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_link_checker.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_pkg_get_pacakges_to_publish
        # Workflow Edge: task_pkg_get_pacakges_to_publish -> task_pkg_assemble_packages
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_pkg_get_pacakges_to_publish")
        print("=" * 80)

        task_prompt = """Please analyze the following monorepo directories and identify packages that need pnpm publishing:
CRITICAL: This step is about planning. We do not want to build anything. All packages MUST be placed in the correct order.

Publish Requirements:
- @mastra/core first, MUST be before any other package
- all packages in correct dependency order before building
- Identify packages that have changes requiring a new pnpm publish
- Include create-mastra in the packages list if changes exist
- EXCLUDE @mastra/dane from consideration

Please list all packages that need building grouped by their directory.
DO NOT NOT USE the 'pnpmBuild' tool during this step. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_package_publisher, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_package_publisher.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_pkg_assemble_packages
        # Workflow Edge: task_pkg_assemble_packages -> task_pkg_build_packages
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_pkg_assemble_packages")
        print("=" * 80)

        task_prompt = """Assemble file system paths for the packages reported by the agent and prepare build sets """
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
        # Workflow Step: task_pkg_build_packages
        # Workflow Edge: task_pkg_build_packages -> task_pkg_verify_build
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_pkg_build_packages")
        print("=" * 80)

        task_prompt = """Build packages using pnpmBuild tool for each package path (sequential and parallel phases) """
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
        # Workflow Step: task_pkg_verify_build
        # Workflow Edge: task_pkg_verify_build -> task_pkg_publish_changeset
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_pkg_verify_build")
        print("=" * 80)

        task_prompt = """Verify dist artifacts exist for all built packages """
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
        # Workflow Step: task_pkg_publish_changeset
        # Workflow Edge: task_pkg_publish_changeset -> task_pkg_set_latest_dist_tag
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_pkg_publish_changeset")
        print("=" * 80)

        task_prompt = """All packages have been built and verified. Publish the changeset for the verified packages and ensure atomic publish and error reporting. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_package_publisher, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_package_publisher.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_pkg_set_latest_dist_tag
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_pkg_set_latest_dist_tag")
        print("=" * 80)

        task_prompt = """Update npm dist-tag for published packages (agent assisted) """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane_package_publisher, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane_package_publisher.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_tel_step_a1
        # Workflow Edge: task_tel_step_a1 -> task_tel_step_a2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_tel_step_a1")
        print("=" * 80)

        task_prompt = """Create starting message for telephone game """
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
        # Workflow Step: task_tel_step_a2
        # Workflow Edge: task_tel_step_a2 -> task_tel_step_b2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_tel_step_a2")
        print("=" * 80)

        task_prompt = """Prompt user for a message (inquirer input) """
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
        # Workflow Step: task_tel_step_b2
        # Workflow Edge: task_tel_step_b2 -> task_tel_step_c2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_tel_step_b2")
        print("=" * 80)

        task_prompt = """Validate that the input message exists and pass through """
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
        # Workflow Step: task_tel_step_c2
        # Workflow Edge: task_tel_step_c2 -> task_tel_step_d2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_tel_step_c2")
        print("=" * 80)

        task_prompt = """When user confirms modification, call the haiku model to alter the message. Only return the new message. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: dane, passing the
        # accumulated history so this step can see every prior step's output.
        result = await dane.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_tel_step_d2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_tel_step_d2")
        print("=" * 80)

        task_prompt = """Pass the final message to the next participant or output """
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