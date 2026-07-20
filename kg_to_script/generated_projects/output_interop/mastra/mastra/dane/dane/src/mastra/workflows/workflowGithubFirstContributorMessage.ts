/**
 * Workflow: workflow_github_first_contributor_message
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { daneNewContributor } from '../agents'

// ── Workflow Steps ──

const taskFirstGetPullRequest = createStep({
  id: 'task_first_get_pull_request',
  description: `Retrieve pull request data from GitHub integration and fetch diff`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Retrieve pull request data from GitHub integration and fetch diff
    // TODO: Implement step logic
    throw new Error('task_first_get_pull_request not implemented yet')
  },
})

const taskFirstMessageGenerator = createStep({
  id: 'task_first_message_generator',
  description: `Given PR title, body, and diff plus Mastra docs, generate a friendly intro, a checklist (if applicable), and an outro thanking the contributor. Do not summarize code or give code advice.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Given PR title, body, and diff plus Mastra docs, generate a friendly intro, a checklist (if applicable), and an outro thanking the contributor. Do not summarize code or give code advice.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await daneNewContributor.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskFirstCreateMessage = createStep({
  id: 'task_first_create_message',
  description: `Post generated message as GitHub issue comment using github integration`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Post generated message as GitHub issue comment using github integration
    // TODO: Implement step logic
    throw new Error('task_first_create_message not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * workflow_github_first_contributor_message
 */
export const workflowGithubFirstContributorMessage = createWorkflow({
  id: 'workflow_github_first_contributor_message',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskFirstGetPullRequest, taskFirstMessageGenerator, taskFirstCreateMessage],
})
  .then(taskFirstGetPullRequest)
  .then(taskFirstMessageGenerator)
  .then(taskFirstCreateMessage)
  .commit()
