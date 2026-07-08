/**
 * Workflow: workflow_telephone_game
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { dane } from '../agents'

// ── Workflow Steps ──

const taskTelStepA1 = createStep({
  id: 'task_tel_step_a1',
  description: `Create starting message for telephone game`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Create starting message for telephone game
    // TODO: Implement step logic
    throw new Error('task_tel_step_a1 not implemented yet')
  },
})

const taskTelStepA2 = createStep({
  id: 'task_tel_step_a2',
  description: `Prompt user for a message (inquirer input)`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Prompt user for a message (inquirer input)
    // TODO: Implement step logic
    throw new Error('task_tel_step_a2 not implemented yet')
  },
})

const taskTelStepB2 = createStep({
  id: 'task_tel_step_b2',
  description: `Validate that the input message exists and pass through`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Validate that the input message exists and pass through
    // TODO: Implement step logic
    throw new Error('task_tel_step_b2 not implemented yet')
  },
})

const taskTelStepC2 = createStep({
  id: 'task_tel_step_c2',
  description: `When user confirms modification, call the haiku model to alter the message. Only return the new message.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `When user confirms modification, call the haiku model to alter the message. Only return the new message.`
    const result = await dane.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskTelStepD2 = createStep({
  id: 'task_tel_step_d2',
  description: `Pass the final message to the next participant or output`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Pass the final message to the next participant or output
    // TODO: Implement step logic
    throw new Error('task_tel_step_d2 not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * workflow_telephone_game
 */
export const workflowTelephoneGame = createWorkflow({
  id: 'workflow_telephone_game',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskTelStepA1, taskTelStepA2, taskTelStepB2, taskTelStepC2, taskTelStepD2],
})
  .then(taskTelStepA1)
  .then(taskTelStepA2)
  .then(taskTelStepB2)
  .then(taskTelStepC2)
  .then(taskTelStepD2)
  .commit()
