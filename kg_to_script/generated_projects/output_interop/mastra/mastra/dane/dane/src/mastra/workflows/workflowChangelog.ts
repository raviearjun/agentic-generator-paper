/**
 * Workflow: workflow_changelog
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { daneChangeLog } from '../agents'

// ── Workflow Steps ──

const taskChangelogStepA1 = createStep({
  id: 'task_changelog_step_a1',
  description: `Get a git diff and connect to slack; runs git diff via execa`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Get a git diff and connect to slack; runs git diff via execa
    // TODO: Implement step logic
    throw new Error('task_changelog_step_a1 not implemented yet')
  },
})

const taskChangelogStepA2 = createStep({
  id: 'task_changelog_step_a2',
  description: `Time: recent week`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Time: recent week
Git diff to generate from: (git diff from previous step)
Task:
1. create a structured narrative changelog that highlights key updates and improvements.
2. Include what packages were changed
Structure: Opening, Major Updates, Technical Improvements, Documentation & Examples, Bug Fixes & Infrastructure
Finally send this to the configured slack channel with slack_post_message tool.`
    const result = await daneChangeLog.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_changelog
 */
export const workflowChangelog = createWorkflow({
  id: 'workflow_changelog',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskChangelogStepA1, taskChangelogStepA2],
})
  .then(taskChangelogStepA1)
  .then(taskChangelogStepA2)
  .commit()
