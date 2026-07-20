/**
 * Workflow: workflow_commit_message
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { daneCommitMessage } from '../agents'

// ── Workflow Steps ──

const taskCommitGetDiff = createStep({
  id: 'task_commit_get_diff',
  description: `Compute git diff of staged changes via git command`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Compute git diff of staged changes via git command
    // TODO: Implement step logic
    throw new Error('task_commit_get_diff not implemented yet')
  },
})

const taskCommitReadConventionalCommitSpec = createStep({
  id: 'task_commit_read_conventional_commit_spec',
  description: `Read conventional commit spec using fsTool`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Read conventional commit spec using fsTool
    // TODO: Implement step logic
    throw new Error('task_commit_read_conventional_commit_spec not implemented yet')
  },
})

const taskCommitGenerateMessage = createStep({
  id: 'task_commit_generate_message',
  description: `Given the git diff, generate a conventional commit message; obey guidelines (start with verb, concise, first line <50 chars, add body if needed). Return commitMessage, generated flag, and guidelines array.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Given the git diff, generate a conventional commit message; obey guidelines (start with verb, concise, first line <50 chars, add body if needed). Return commitMessage, generated flag, and guidelines array.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await daneCommitMessage.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskCommitConfirmation = createStep({
  id: 'task_commit_confirmation',
  description: `Prompt human user to confirm commit message via inquirer confirm`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Prompt human user to confirm commit message via inquirer confirm
    // TODO: Implement step logic
    throw new Error('task_commit_confirmation not implemented yet')
  },
})

const taskCommitCommit = createStep({
  id: 'task_commit_commit',
  description: `Perform git commit with generated message (execSync git commit)`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Perform git commit with generated message (execSync git commit)
    // TODO: Implement step logic
    throw new Error('task_commit_commit not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * workflow_commit_message
 */
export const workflowCommitMessage = createWorkflow({
  id: 'workflow_commit_message',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskCommitGetDiff, taskCommitReadConventionalCommitSpec, taskCommitGenerateMessage, taskCommitConfirmation, taskCommitCommit],
})
  .then(taskCommitGetDiff)
  .then(taskCommitReadConventionalCommitSpec)
  .then(taskCommitGenerateMessage)
  .then(taskCommitConfirmation)
  .then(taskCommitCommit)
  .commit()
