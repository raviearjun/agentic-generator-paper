/**
 * Workflow: workflow_link_checker
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { daneLinkChecker } from '../agents'

// ── Workflow Steps ──

const taskLinkGetBrokenLinks = createStep({
  id: 'task_link_get_broken_links',
  description: `Run linkinator via shell to collect links; parse JSON output`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Run linkinator via shell to collect links; parse JSON output
    // TODO: Implement step logic
    throw new Error('task_link_get_broken_links not implemented yet')
  },
})

const taskLinkReportBrokenLinks = createStep({
  id: 'task_link_report_broken_links',
  description: `Format the broken links JSON into a human-friendly Slack message and send to the configured channel using slack_post_message tool.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Format the broken links JSON into a human-friendly Slack message and send to the configured channel using slack_post_message tool.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await daneLinkChecker.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_link_checker
 */
export const workflowLinkChecker = createWorkflow({
  id: 'workflow_link_checker',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskLinkGetBrokenLinks, taskLinkReportBrokenLinks],
})
  .then(taskLinkGetBrokenLinks)
  .then(taskLinkReportBrokenLinks)
  .commit()
