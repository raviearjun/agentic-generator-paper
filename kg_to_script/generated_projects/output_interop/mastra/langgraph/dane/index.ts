import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraDaneprojectinstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
