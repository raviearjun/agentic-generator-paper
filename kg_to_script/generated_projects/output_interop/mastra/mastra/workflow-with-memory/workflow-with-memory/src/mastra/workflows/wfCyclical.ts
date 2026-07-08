/**
 * Workflow: wf_cyclical
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow with conditional and cyclical step references defined in src/mastra/workflows/index.ts
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { catOne } from '../agents'

// ── Workflow Steps ──

const taskCycStepOne = createStep({
  id: 'task_cyc_step_one',
  description: `Doubles the input value`,
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({valueToIncrement: z.number()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Doubles the input value`
    const result = await catOne.generate(prompt)
    return {
      ...context,
      valueToIncrement: context.valueToIncrement ?? result.text,
    }
  },
})

const taskCycStepTwo = createStep({
  id: 'task_cyc_step_two',
  description: `Adds 1 to the input value`,
  inputSchema: z.object({valueToIncrement: z.number()}),
  outputSchema: z.object({valueToSquare: z.number()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Adds 1 to the input value`
    const result = await catOne.generate(prompt)
    return {
      ...context,
      valueToSquare: context.valueToSquare ?? result.text,
    }
  },
})

const taskCycStepThree = createStep({
  id: 'task_cyc_step_three',
  description: `Squares the input value`,
  inputSchema: z.object({valueToSquare: z.number()}),
  outputSchema: z.object({inputValue: z.number()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Squares the input value`
    const result = await catOne.generate(prompt)
    return {
      ...context,
      inputValue: context.inputValue ?? result.text,
    }
  },
})

const taskCycStepOneLoop = createStep({
  id: 'task_cyc_step_one_loop',
  description: `Doubles the input value (loop invocation)`,
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Doubles the input value (loop invocation)`
    const result = await catOne.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wf_cyclical
 *
 * Workflow with conditional and cyclical step references defined in src/mastra/workflows/index.ts
 */
export const wfCyclical = createWorkflow({
  id: 'wf_cyclical',
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({}),
  steps: [taskCycStepOne, taskCycStepTwo, taskCycStepThree, taskCycStepOneLoop],
})
  // NOTE: Branching workflow — simplified to sequential for type compatibility
  // TODO: Implement conditional branching using .branch() API
  .then(taskCycStepOne)
  .then(taskCycStepTwo)
  .then(taskCycStepThree)
  .then(taskCycStepOneLoop)
  .commit()
