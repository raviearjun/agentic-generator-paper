/**
 * Workflow: my_workflow_pattern
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { mastraAgent } from '../agents'

// ── Workflow Steps ──

const taskStepOne = createStep({
  id: 'task_step_one',
  description: `Doubles triggerData.inputValue and returns an object with { doubledValue }.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Doubles triggerData.inputValue and returns an object with { doubledValue }.`
    const result = await mastraAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskStepThree = createStep({
  id: 'task_step_three',
  description: `Triples triggerData.inputValue and returns an object with { tripledValue }.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Triples triggerData.inputValue and returns an object with { tripledValue }.`
    const result = await mastraAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskStepTwo = createStep({
  id: 'task_step_two',
  description: `Reads the payload from stepOne (doubledValue) and returns an object with { incrementedValue } which is doubledValue + 1.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Reads the payload from stepOne (doubledValue) and returns an object with { incrementedValue } which is doubledValue + 1.`
    const result = await mastraAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskStepFour = createStep({
  id: 'task_step_four',
  description: `Reads the payload from stepThree (tripledValue) and returns an object with { isEven } indicating whether tripledValue is even.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Reads the payload from stepThree (tripledValue) and returns an object with { isEven } indicating whether tripledValue is even.`
    const result = await mastraAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * my_workflow_pattern
 */
export const myWorkflowPattern = createWorkflow({
  id: 'my_workflow_pattern',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskStepOne, taskStepThree, taskStepTwo, taskStepFour],
})
  .then(taskStepOne)
  .then(taskStepThree)
  .then(taskStepTwo)
  .then(taskStepFour)
  .commit()
