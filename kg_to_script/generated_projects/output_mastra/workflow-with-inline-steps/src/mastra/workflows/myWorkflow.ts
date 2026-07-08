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
  description: `Execute: doubledValue = context.machineContext.triggerData.inputValue * 2`,
  inputSchema: z.object({Execute: z.number()}),
  outputSchema: z.object({then_incrementedValue: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Execute: doubledValue = context.machineContext.triggerData.inputValue * 2`
    const result = await mastraDefaultAgent.generate(prompt)
    return {
      ...context,
      then_incrementedValue: context.then_incrementedValue ?? result.text,
    }
  },
})

const taskStepTwo = createStep({
  id: 'task_step_two',
  description: `If context.machineContext.stepResults.stepOne.status == 'success' then incrementedValue = context.machineContext.stepResults.stepOne.payload.doubledValue + 1 else incrementedValue = 0`,
  inputSchema: z.object({then_incrementedValue: z.string()}),
  outputSchema: z.object({incrementedValue: z.number()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `If context.machineContext.stepResults.stepOne.status == 'success' then incrementedValue = context.machineContext.stepResults.stepOne.payload.doubledValue + 1 else incrementedValue = 0`
    const result = await mastraDefaultAgent.generate(prompt)
    return {
      ...context,
      incrementedValue: context.incrementedValue ?? result.text,
    }
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
  inputSchema: z.object({Execute: z.number()}),
  outputSchema: z.object({incrementedValue: z.number()}),
  steps: [taskStepOne, taskStepTwo],
})
  .then(taskStepOne)
  .then(taskStepTwo)
  .commit()
