import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraDaneprojectinstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_browser_tool
const tool_browser_tool = tool(
  async () => {
    return "Result of tool_browser_tool";
  },
  {
    name: "tool_browser_tool",
    description: "Opens a headless browser, navigates to a URL and captures content; chunks HTML into documents.",
    schema: z.object({}),
  }
);
// Tool: tool_google_search
const tool_google_search = tool(
  async () => {
    return "Result of tool_google_search";
  },
  {
    name: "tool_google_search",
    description: "Performs a Google search by opening search results and extracting links.",
    schema: z.object({}),
  }
);
// Tool: tool_list_events
const tool_list_events = tool(
  async () => {
    return "Result of tool_list_events";
  },
  {
    name: "tool_list_events",
    description: "Reads local (Mac) Calendar events via AppleScript and returns events.",
    schema: z.object({}),
  }
);
// Tool: tool_crawl
const tool_crawl = tool(
  async () => {
    return "Result of tool_crawl";
  },
  {
    name: "tool_crawl",
    description: "Triggers Firecrawl integration to crawl and sync website content.",
    schema: z.object({}),
  }
);
// Tool: tool_execa_tool
const tool_execa_tool = tool(
  async () => {
    return "Result of tool_execa_tool";
  },
  {
    name: "tool_execa_tool",
    description: "Execute shell commands and stream output.",
    schema: z.object({}),
  }
);
// Tool: tool_fs_tool
const tool_fs_tool = tool(
  async () => {
    return "Result of tool_fs_tool";
  },
  {
    name: "tool_fs_tool",
    description: "Read, write, and append files on local filesystem.",
    schema: z.object({}),
  }
);
// Tool: tool_image_tool
const tool_image_tool = tool(
  async () => {
    return "Result of tool_image_tool";
  },
  {
    name: "tool_image_tool",
    description: "Generate images using Stability AI integration and save to disk.",
    schema: z.object({}),
  }
);
// Tool: tool_read_pdf
const tool_read_pdf = tool(
  async () => {
    return "Result of tool_read_pdf";
  },
  {
    name: "tool_read_pdf",
    description: "Parse PDF files and return extracted text.",
    schema: z.object({}),
  }
);
// Tool: tool_pnpm_build
const tool_pnpm_build = tool(
  async () => {
    return "Result of tool_pnpm_build";
  },
  {
    name: "tool_pnpm_build",
    description: "Runs pnpm build in package directories.",
    schema: z.object({}),
  }
);
// Tool: tool_pnpm_changeset_status
const tool_pnpm_changeset_status = tool(
  async () => {
    return "Result of tool_pnpm_changeset_status";
  },
  {
    name: "tool_pnpm_changeset_status",
    description: "Check which pnpm modules would be published via dry-run.",
    schema: z.object({}),
  }
);
// Tool: tool_pnpm_changeset_publish
const tool_pnpm_changeset_publish = tool(
  async () => {
    return "Result of tool_pnpm_changeset_publish";
  },
  {
    name: "tool_pnpm_changeset_publish",
    description: "Publish pnpm changesets.",
    schema: z.object({}),
  }
);
// Tool: tool_active_dist_tag
const tool_active_dist_tag = tool(
  async () => {
    return "Result of tool_active_dist_tag";
  },
  {
    name: "tool_active_dist_tag",
    description: "Set npm dist-tag on published packages.",
    schema: z.object({}),
  }
);
// Tool: tool_slack_client
const tool_slack_client = tool(
  async () => {
    return "Result of tool_slack_client";
  },
  {
    name: "tool_slack_client",
    description: "Mastra MCP client for Slack, runs a docker command to post messages.",
    schema: z.object({}),
  }
);
// Tool: tool_firecrawl_integration
const tool_firecrawl_integration = tool(
  async () => {
    return "Result of tool_firecrawl_integration";
  },
  {
    name: "tool_firecrawl_integration",
    description: "Integration to crawl and sync content using Firecrawl API.",
    schema: z.object({}),
  }
);
// Tool: tool_github_integration
const tool_github_integration = tool(
  async () => {
    return "Result of tool_github_integration";
  },
  {
    name: "tool_github_integration",
    description: "GitHub API integration for retrieving PRs, issues and posting comments.",
    schema: z.object({}),
  }
);
// Tool: tool_stabilityai_integration
const tool_stabilityai_integration = tool(
  async () => {
    return "Result of tool_stabilityai_integration";
  },
  {
    name: "tool_stabilityai_integration",
    description: "Integration to generate images using Stability AI API.",
    schema: z.object({}),
  }
);
// Tool: tool_upstash_store
const tool_upstash_store = tool(
  async () => {
    return "Result of tool_upstash_store";
  },
  {
    name: "tool_upstash_store",
    description: "Upstash HTTP store used by Memory; token-based auth.",
    schema: z.object({}),
  }
);



/**
 * Node: taskChangelogStepA1
 * Agent: dane
 */
async function taskChangelogStepA1(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Get a git diff and connect to slack; runs git diff via execa" +
        "\nNode: taskChangelogStepA1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskChangelogStepA2
 * Agent: dane_change_log
 */
async function taskChangelogStepA2(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a changelog_writer." +
        "\n\nYour task: Time: recent week\nGit diff to generate from: (git diff from previous step)\nTask:\n1. create a structured narrative changelog that highlights key updates and improvements.\n2. Include what packages were changed\nStructure: Opening, Major Updates, Technical Improvements, Documentation & Examples, Bug Fixes & Infrastructure\nFinally send this to the configured slack channel with slack_post_message tool." +
        "\nNode: taskChangelogStepA2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskEntryMessageInput
 * Agent: dane
 */
async function taskEntryMessageInput(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Prompt user to input a message (inquirer prompt)" +
        "\nNode: taskEntryMessageInput",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskEntryMessageOutput
 * Agent: dane
 */
async function taskEntryMessageOutput(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: User-supplied message forwarded to Dane agent for response; context includes threadId and resourceId." +
        "\nNode: taskEntryMessageOutput",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCommitGetDiff
 * Agent: dane
 */
async function taskCommitGetDiff(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Compute git diff of staged changes via git command" +
        "\nNode: taskCommitGetDiff",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCommitReadConventionalCommitSpec
 * Agent: dane
 */
async function taskCommitReadConventionalCommitSpec(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Read conventional commit spec using fsTool" +
        "\nNode: taskCommitReadConventionalCommitSpec",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCommitGenerateMessage
 * Agent: dane_commit_message
 */
async function taskCommitGenerateMessage(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a commit_message_generator." +
        "\n\nYour task: Given the git diff, generate a conventional commit message; obey guidelines (start with verb, concise, first line <50 chars, add body if needed). Return commitMessage, generated flag, and guidelines array." +
        "\nNode: taskCommitGenerateMessage",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCommitConfirmation
 * Agent: dane
 */
async function taskCommitConfirmation(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Prompt human user to confirm commit message via inquirer confirm" +
        "\nNode: taskCommitConfirmation",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCommitCommit
 * Agent: dane
 */
async function taskCommitCommit(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Perform git commit with generated message (execSync git commit)" +
        "\nNode: taskCommitCommit",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFirstGetPullRequest
 * Agent: dane
 */
async function taskFirstGetPullRequest(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Retrieve pull request data from GitHub integration and fetch diff" +
        "\nNode: taskFirstGetPullRequest",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFirstMessageGenerator
 * Agent: dane_new_contributor
 */
async function taskFirstMessageGenerator(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a new_contributor_messaging." +
        "\n\nYour task: Given PR title, body, and diff plus Mastra docs, generate a friendly intro, a checklist (if applicable), and an outro thanking the contributor. Do not summarize code or give code advice." +
        "\nNode: taskFirstMessageGenerator",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFirstCreateMessage
 * Agent: dane
 */
async function taskFirstCreateMessage(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Post generated message as GitHub issue comment using github integration" +
        "\nNode: taskFirstCreateMessage",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskIssueGetIssue
 * Agent: dane
 */
async function taskIssueGetIssue(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Retrieve issue and repository labels using GitHub integration" +
        "\nNode: taskIssueGetIssue",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskIssueLabelIssue
 * Agent: dane_issue_labeler
 */
async function taskIssueLabelIssue(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a issue_labeler." +
        "\n\nYour task: Given issue title, body, and available repo labels, propose one or more labels to assign." +
        "\nNode: taskIssueLabelIssue",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskIssueApplyLabels
 * Agent: dane
 */
async function taskIssueApplyLabels(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Add labels to GitHub issue using integrations client" +
        "\nNode: taskIssueApplyLabels",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskLinkGetBrokenLinks
 * Agent: dane
 */
async function taskLinkGetBrokenLinks(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Run linkinator via shell to collect links; parse JSON output" +
        "\nNode: taskLinkGetBrokenLinks",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskLinkReportBrokenLinks
 * Agent: dane_link_checker
 */
async function taskLinkReportBrokenLinks(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a link_checker." +
        "\n\nYour task: Format the broken links JSON into a human-friendly Slack message and send to the configured channel using slack_post_message tool." +
        "\nNode: taskLinkReportBrokenLinks",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPkgGetPacakgesToPublish
 * Agent: dane_package_publisher
 */
async function taskPkgGetPacakgesToPublish(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a package_publisher." +
        "\n\nYour task: Please analyze the following monorepo directories and identify packages that need pnpm publishing:\nCRITICAL: This step is about planning. We do not want to build anything. All packages MUST be placed in the correct order.\n\nPublish Requirements:\n- @mastra/core first, MUST be before any other package\n- all packages in correct dependency order before building\n- Identify packages that have changes requiring a new pnpm publish\n- Include create-mastra in the packages list if changes exist\n- EXCLUDE @mastra/dane from consideration\n\nPlease list all packages that need building grouped by their directory.\nDO NOT NOT USE the 'pnpmBuild' tool during this step." +
        "\nNode: taskPkgGetPacakgesToPublish",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPkgAssemblePackages
 * Agent: dane
 */
async function taskPkgAssemblePackages(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Assemble file system paths for the packages reported by the agent and prepare build sets" +
        "\nNode: taskPkgAssemblePackages",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPkgBuildPackages
 * Agent: dane
 */
async function taskPkgBuildPackages(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Build packages using pnpmBuild tool for each package path (sequential and parallel phases)" +
        "\nNode: taskPkgBuildPackages",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPkgVerifyBuild
 * Agent: dane
 */
async function taskPkgVerifyBuild(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Verify dist artifacts exist for all built packages" +
        "\nNode: taskPkgVerifyBuild",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPkgPublishChangeset
 * Agent: dane_package_publisher
 */
async function taskPkgPublishChangeset(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a package_publisher." +
        "\n\nYour task: All packages have been built and verified. Publish the changeset for the verified packages and ensure atomic publish and error reporting." +
        "\nNode: taskPkgPublishChangeset",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPkgSetLatestDistTag
 * Agent: dane_package_publisher
 */
async function taskPkgSetLatestDistTag(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a package_publisher." +
        "\n\nYour task: Update npm dist-tag for published packages (agent assisted)" +
        "\nNode: taskPkgSetLatestDistTag",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTelStepA1
 * Agent: dane
 */
async function taskTelStepA1(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Create starting message for telephone game" +
        "\nNode: taskTelStepA1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTelStepA2
 * Agent: dane
 */
async function taskTelStepA2(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Prompt user for a message (inquirer input)" +
        "\nNode: taskTelStepA2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTelStepB2
 * Agent: dane
 */
async function taskTelStepB2(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Validate that the input message exists and pass through" +
        "\nNode: taskTelStepB2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTelStepC2
 * Agent: dane
 */
async function taskTelStepC2(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: When user confirms modification, call the haiku model to alter the message. Only return the new message." +
        "\nNode: taskTelStepC2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTelStepD2
 * Agent: dane
 */
async function taskTelStepD2(state: typeof MastraDaneprojectinstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: Pass the final message to the next participant or output" +
        "\nNode: taskTelStepD2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraDaneprojectinstanceAnnotation)
  .addNode("taskChangelogStepA1", taskChangelogStepA1)
  .addNode("taskChangelogStepA2", taskChangelogStepA2)
  .addNode("taskEntryMessageInput", taskEntryMessageInput)
  .addNode("taskEntryMessageOutput", taskEntryMessageOutput)
  .addNode("taskCommitGetDiff", taskCommitGetDiff)
  .addNode("taskCommitReadConventionalCommitSpec", taskCommitReadConventionalCommitSpec)
  .addNode("taskCommitGenerateMessage", taskCommitGenerateMessage)
  .addNode("taskCommitConfirmation", taskCommitConfirmation)
  .addNode("taskCommitCommit", taskCommitCommit)
  .addNode("taskFirstGetPullRequest", taskFirstGetPullRequest)
  .addNode("taskFirstMessageGenerator", taskFirstMessageGenerator)
  .addNode("taskFirstCreateMessage", taskFirstCreateMessage)
  .addNode("taskIssueGetIssue", taskIssueGetIssue)
  .addNode("taskIssueLabelIssue", taskIssueLabelIssue)
  .addNode("taskIssueApplyLabels", taskIssueApplyLabels)
  .addNode("taskLinkGetBrokenLinks", taskLinkGetBrokenLinks)
  .addNode("taskLinkReportBrokenLinks", taskLinkReportBrokenLinks)
  .addNode("taskPkgGetPacakgesToPublish", taskPkgGetPacakgesToPublish)
  .addNode("taskPkgAssemblePackages", taskPkgAssemblePackages)
  .addNode("taskPkgBuildPackages", taskPkgBuildPackages)
  .addNode("taskPkgVerifyBuild", taskPkgVerifyBuild)
  .addNode("taskPkgPublishChangeset", taskPkgPublishChangeset)
  .addNode("taskPkgSetLatestDistTag", taskPkgSetLatestDistTag)
  .addNode("taskTelStepA1", taskTelStepA1)
  .addNode("taskTelStepA2", taskTelStepA2)
  .addNode("taskTelStepB2", taskTelStepB2)
  .addNode("taskTelStepC2", taskTelStepC2)
  .addNode("taskTelStepD2", taskTelStepD2)
  .addEdge(START, "taskChangelogStepA1")
  .addEdge("taskEntryMessageInput", "taskEntryMessageOutput")
  .addEdge("taskCommitGetDiff", "taskCommitReadConventionalCommitSpec")
  .addEdge("taskCommitReadConventionalCommitSpec", "taskCommitGenerateMessage")
  .addEdge("taskCommitGenerateMessage", "taskCommitConfirmation")
  .addEdge("taskCommitConfirmation", "taskCommitCommit")
  .addEdge("taskFirstGetPullRequest", "taskFirstMessageGenerator")
  .addEdge("taskFirstMessageGenerator", "taskFirstCreateMessage")
  .addEdge("taskIssueGetIssue", "taskIssueLabelIssue")
  .addEdge("taskIssueLabelIssue", "taskIssueApplyLabels")
  .addEdge("taskLinkGetBrokenLinks", "taskLinkReportBrokenLinks")
  .addEdge("taskPkgGetPacakgesToPublish", "taskPkgAssemblePackages")
  .addEdge("taskPkgAssemblePackages", "taskPkgBuildPackages")
  .addEdge("taskPkgBuildPackages", "taskPkgVerifyBuild")
  .addEdge("taskPkgVerifyBuild", "taskPkgPublishChangeset")
  .addEdge("taskPkgPublishChangeset", "taskPkgSetLatestDistTag")
  .addEdge("taskTelStepA1", "taskTelStepA2")
  .addEdge("taskTelStepA2", "taskTelStepB2")
  .addEdge("taskTelStepB2", "taskTelStepC2")
  .addEdge("taskTelStepC2", "taskTelStepD2")
  .addEdge("taskChangelogStepA1", END)
  .addEdge("taskEntryMessageOutput", END)
  .addEdge("taskCommitCommit", END)
  .addEdge("taskFirstCreateMessage", END)
  .addEdge("taskIssueApplyLabels", END)
  .addEdge("taskLinkReportBrokenLinks", END)
  .addEdge("taskPkgSetLatestDistTag", END)
  .addEdge("taskTelStepD2", END)
;

export const graph = workflow.compile();
graph.name = "MastraDaneprojectinstance";
// Workflow: workflow_changelog
// Workflow: workflow_entry
// Workflow: workflow_commit_message
// Workflow: workflow_github_first_contributor_message
// Workflow: workflow_github_issue_labeler
// Workflow: workflow_link_checker
// Workflow: workflow_pnpm_changset_publisher
// Workflow: workflow_telephone_game
