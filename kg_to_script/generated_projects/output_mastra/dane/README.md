# MastraDaneprojectinstance

Mastra instance bundling agents, tools, memory and workflows for the Dane assistant CLI project.

**Auto-generated from AgentO Knowledge Graph**  
Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

### 3. Run the Project

```bash
npm run dev
```

---

## 📦 Project Structure

```
MastraDaneprojectinstance/
├── src/
│   └── mastra/
│       ├── index.ts           # Mastra instance + registrations
│       ├── agents/            # Agent definitions
│       │   └── dane.ts
│       │   └── daneCommitMessage.ts
│       │   └── daneIssueLabeler.ts
│       │   └── daneLinkChecker.ts
│       │   └── daneChangeLog.ts
│       │   └── daneNewContributor.ts
│       │   └── danePackagePublisher.ts
│       ├── tools/             # Tool definitions
│       │   └── toolBrowserTool.ts
│       │   └── toolGoogleSearch.ts
│       │   └── toolListEvents.ts
│       │   └── toolCrawl.ts
│       │   └── toolExecaTool.ts
│       │   └── toolFsTool.ts
│       │   └── toolImageTool.ts
│       │   └── toolReadPdf.ts
│       │   └── toolPnpmBuild.ts
│       │   └── toolPnpmChangesetStatus.ts
│       │   └── toolPnpmChangesetPublish.ts
│       │   └── toolActiveDistTag.ts
│       │   └── toolSlackClient.ts
│       │   └── toolFirecrawlIntegration.ts
│       │   └── toolGithubIntegration.ts
│       │   └── toolStabilityaiIntegration.ts
│       │   └── toolUpstashStore.ts
│       └── workflows/         # Workflow definitions
│           └── workflowChangelog.ts
│           └── workflowEntry.ts
│           └── workflowCommitMessage.ts
│           └── workflowGithubFirstContributorMessage.ts
│           └── workflowGithubIssueLabeler.ts
│           └── workflowLinkChecker.ts
│           └── workflowPnpmChangsetPublisher.ts
│           └── workflowTelephoneGame.ts
├── package.json
├── tsconfig.json
└── .env.example
```

---

## 🤖 Agents

### assistant

- **ID:** `Dane`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolBrowserTool, toolGoogleSearch, toolListEvents, toolCrawl, toolExecaTool, toolFsTool, toolImageTool, toolReadPdf

You are assistant....

### commit_message_generator

- **ID:** `DaneCommitMessage`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolFsTool

You are commit_message_generator....

### issue_labeler

- **ID:** `DaneIssueLabeler`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolGithubIntegration

You are issue_labeler....

### link_checker

- **ID:** `DaneLinkChecker`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolSlackClient

You are link_checker....

### changelog_writer

- **ID:** `DaneChangeLog`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolSlackClient

You are changelog_writer....

### new_contributor_messaging

- **ID:** `DaneNewContributor`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolGithubIntegration

You are new_contributor_messaging....

### package_publisher

- **ID:** `DanePackagePublisher`
- **Model:** `openai/gpt-4o-mini`
- **Tools:** toolPnpmBuild, toolPnpmChangesetStatus, toolPnpmChangesetPublish, toolActiveDistTag

You are package_publisher....


---

## 🔧 Tools

### toolBrowserTool

Opens a headless browser, navigates to a URL and captures content; chunks HTML into documents....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolBrowserTool.ts`)

### toolGoogleSearch

Performs a Google search by opening search results and extracting links....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolGoogleSearch.ts`)

### toolListEvents

Reads local (Mac) Calendar events via AppleScript and returns events....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolListEvents.ts`)

### toolCrawl

Triggers Firecrawl integration to crawl and sync website content....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolCrawl.ts`)

### toolExecaTool

Execute shell commands and stream output....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolExecaTool.ts`)

### toolFsTool

Read, write, and append files on local filesystem....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolFsTool.ts`)

### toolImageTool

Generate images using Stability AI integration and save to disk....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolImageTool.ts`)

### toolReadPdf

Parse PDF files and return extracted text....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolReadPdf.ts`)

### toolPnpmBuild

Runs pnpm build in package directories....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolPnpmBuild.ts`)

### toolPnpmChangesetStatus

Check which pnpm modules would be published via dry-run....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolPnpmChangesetStatus.ts`)

### toolPnpmChangesetPublish

Publish pnpm changesets....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolPnpmChangesetPublish.ts`)

### toolActiveDistTag

Set npm dist-tag on published packages....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolActiveDistTag.ts`)

### toolSlackClient

Mastra MCP client for Slack, runs a docker command to post messages....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolSlackClient.ts`)

### toolFirecrawlIntegration

Integration to crawl and sync content using Firecrawl API....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolFirecrawlIntegration.ts`)

### toolGithubIntegration

GitHub API integration for retrieving PRs, issues and posting comments....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolGithubIntegration.ts`)

### toolStabilityaiIntegration

Integration to generate images using Stability AI API....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolStabilityaiIntegration.ts`)

### toolUpstashStore

Upstash HTTP store used by Memory; token-based auth....

**Status:** ⚠️ Implementation required (see TODO in `src/mastra/tools/toolUpstashStore.ts`)


---

## 🔄 Workflows

### workflow_changelog



**Steps:** 2
1. task_changelog_step_a1
2. task_changelog_step_a2

### workflow_entry



**Steps:** 2
1. task_entry_message_input
2. task_entry_message_output

### workflow_commit_message



**Steps:** 5
1. task_commit_get_diff
2. task_commit_read_conventional_commit_spec
3. task_commit_generate_message
4. task_commit_confirmation
5. task_commit_commit

### workflow_github_first_contributor_message



**Steps:** 3
1. task_first_get_pull_request
2. task_first_message_generator
3. task_first_create_message

### workflow_github_issue_labeler



**Steps:** 3
1. task_issue_get_issue
2. task_issue_label_issue
3. task_issue_apply_labels

### workflow_link_checker



**Steps:** 2
1. task_link_get_broken_links
2. task_link_report_broken_links

### workflow_pnpm_changset_publisher



**Steps:** 6
1. task_pkg_get_pacakges_to_publish
2. task_pkg_assemble_packages
3. task_pkg_build_packages
4. task_pkg_verify_build
5. task_pkg_publish_changeset
6. task_pkg_set_latest_dist_tag

### workflow_telephone_game



**Steps:** 5
1. task_tel_step_a1
2. task_tel_step_a2
3. task_tel_step_b2
4. task_tel_step_c2
5. task_tel_step_d2


---

## 📝 Next Steps

1. **Implement tools:** Replace `throw new Error(...)` in tool files with actual implementations
2. **Implement workflow steps:** Add logic to each step's `execute` function
3. **Test agents:** Use Mastra Studio or write test scripts
4. **Deploy:** Follow [Mastra deployment guide](https://mastra.ai/docs/deployment)

---

## 📚 Resources

- [Mastra Documentation](https://mastra.ai/docs)
- [AgentO Ontology](https://w3id.org/agentic-ai/onto)
- [Mastra Discord Community](https://discord.gg/BTYqqHKUrf)

---

**Generated by:** Agentic AI Framework Generator  
**Source:** AgentO Knowledge Graph → Mastra AI TypeScript
