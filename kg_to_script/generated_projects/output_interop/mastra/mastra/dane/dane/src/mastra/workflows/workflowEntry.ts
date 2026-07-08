/**
 * Workflow: workflow_entry
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { dane } from '../agents'

// ── Workflow Steps ──

const taskEntryMessageInput = createStep({
  id: 'task_entry_message_input',
  description: `Prompt user to input a message (inquirer prompt)`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Prompt user to input a message (inquirer prompt)
    // TODO: Implement step logic
    throw new Error('task_entry_message_input not implemented yet')
  },
})

const taskEntryMessageOutput = createStep({
  id: 'task_entry_message_output',
  description: `User-supplied message forwarded to Dane agent for response; context includes threadId and resourceId.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `User-supplied message forwarded to Dane agent for response; context includes threadId and resourceId.`
    const result = await dane.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_entry
 */
export const workflowEntry = createWorkflow({
  id: 'workflow_entry',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskEntryMessageInput, taskEntryMessageOutput],
})
  .then(taskEntryMessageInput)
  .then(taskEntryMessageOutput)
  .commit()
