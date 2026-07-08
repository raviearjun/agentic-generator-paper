/**
 * Workflow: wf_parallel
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow defined in src/mastra/workflows/index.ts (parallel branches)
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { catOne } from '../agents'

// ── Workflow Steps ──

const taskParStepOne = createStep({
  id: 'task_par_step_one',
  description: `Doubles the input value`,
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({inputValue: z.number()}),
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
      inputValue: context.inputValue ?? result.text,
    }
  },
})

const taskParStepSix = createStep({
  id: 'task_par_step_six',
  description: `Logs the input value`,
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({valueToIncrement: z.number()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Logs the input value`
    const result = await catOne.generate(prompt)
    return {
      ...context,
      valueToIncrement: context.valueToIncrement ?? result.text,
    }
  },
})

const taskParStepTwo = createStep({
  id: 'task_par_step_two',
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

const taskParStepThree = createStep({
  id: 'task_par_step_three',
  description: `Squares the input value`,
  inputSchema: z.object({valueToSquare: z.number()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Squares the input value`
    const result = await catOne.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wf_parallel
 *
 * Workflow defined in src/mastra/workflows/index.ts (parallel branches)
 */
export const wfParallel = createWorkflow({
  id: 'wf_parallel',
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({}),
  steps: [taskParStepOne, taskParStepSix, taskParStepTwo, taskParStepThree],
})
  // NOTE: Branching workflow — simplified to sequential for type compatibility
  // TODO: Implement conditional branching using .branch() API
  .then(taskParStepOne)
  .then(taskParStepSix)
  .then(taskParStepTwo)
  .then(taskParStepThree)
  .commit()
