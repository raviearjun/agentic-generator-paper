/**
 * Mastra AI Instance - MastraDaneprojectinstance
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { dane, daneCommitMessage, daneIssueLabeler, daneLinkChecker, daneChangeLog, daneNewContributor, danePackagePublisher } from './agents'

// Import workflows
import { workflowChangelog, workflowEntry, workflowCommitMessage, workflowGithubFirstContributorMessage, workflowGithubIssueLabeler, workflowLinkChecker, workflowPnpmChangsetPublisher, workflowTelephoneGame } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance bundling agents, tools, memory and workflows for the Dane assistant CLI project.
 */
export const mastra = new Mastra({
  agents: {
    dane,
    daneCommitMessage,
    daneIssueLabeler,
    daneLinkChecker,
    daneChangeLog,
    daneNewContributor,
    danePackagePublisher,
  },
  workflows: {
    workflowChangelog,
    workflowEntry,
    workflowCommitMessage,
    workflowGithubFirstContributorMessage,
    workflowGithubIssueLabeler,
    workflowLinkChecker,
    workflowPnpmChangsetPublisher,
    workflowTelephoneGame,
  },
})
