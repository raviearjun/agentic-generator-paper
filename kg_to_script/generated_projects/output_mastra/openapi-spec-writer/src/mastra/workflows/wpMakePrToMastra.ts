/**
 * Workflow: wp_make_pr_to_mastra
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow to format YAML, add files to GitHub and create a PR for the integration.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { openapiSpecGenAgent } from '../agents'

// Import tools used by workflow steps
import { toolAddToGithub } from '../tools'

// ── Workflow Steps ──

const taskAddToGithub = createStep({
  id: 'task_add_to_github',
  description: `Can you take this text blob and format it into proper YAML? Ensure valid OpenAPI syntax and remove surrounding code fences.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Can you take this text blob and format it into proper YAML? Ensure valid OpenAPI syntax and remove surrounding code fences.`
    const result = await openapiSpecGenAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wp_make_pr_to_mastra
 *
 * Workflow to format YAML, add files to GitHub and create a PR for the integration.
 */
export const wpMakePrToMastra = createWorkflow({
  id: 'wp_make_pr_to_mastra',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskAddToGithub],
})
  .then(taskAddToGithub)
  .commit()
