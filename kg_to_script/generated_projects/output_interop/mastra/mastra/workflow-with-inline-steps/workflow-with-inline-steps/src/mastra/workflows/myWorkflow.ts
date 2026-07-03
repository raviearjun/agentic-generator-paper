/**
 * Workflow: my_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow with triggerSchema { inputValue: number } and two sequential inline steps (stepOne -> stepTwo).
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { mastraDefaultAgent } from '../agents'

// ── Workflow Steps ──

const taskStepOne = createStep({
  id: 'task_step_one',
  description: `Compute doubledValue from triggerData.inputValue.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Execute: doubledValue = context.machineContext.triggerData.inputValue * 2
    // This step uses agent: mastraDefaultAgent
    // const result = await mastraDefaultAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_step_one not implemented yet')
  },
})

const taskStepTwo = createStep({
  id: 'task_step_two',
  description: `If stepOne succeeded, compute incrementedValue = doubledValue + 1; else return 0.`,
  inputSchema: z.object({}),
  outputSchema: z.object({incrementedValue: z.number()}),
  execute: async ({ inputData }) => {
    // If context.machineContext.stepResults.stepOne.status == 'success' then incrementedValue = context.machineContext.stepResults.stepOne.payload.doubledValue + 1 else incrementedValue = 0
    // This step uses agent: mastraDefaultAgent
    // const result = await mastraDefaultAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_step_two not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * my_workflow
 *
 * Workflow with triggerSchema { inputValue: number } and two sequential inline steps (stepOne -> stepTwo).
 */
export const myWorkflow = createWorkflow({
  id: 'my_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({incrementedValue: z.number()}),
  steps: [taskStepOne, taskStepTwo],
})
  .then(taskStepOne)
  .then(taskStepTwo)
  .commit()
