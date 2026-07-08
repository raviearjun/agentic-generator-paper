/**
 * Workflow: wf_branched
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow with branching (after and parallel branch) defined in src/mastra/workflows/index.ts
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { catOne } from '../agents'

// ── Workflow Steps ──

const taskBrStepOne = createStep({
  id: 'task_br_step_one',
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

const taskBrStepTwo = createStep({
  id: 'task_br_step_two',
  description: `Adds 1 to the input value`,
  inputSchema: z.object({valueToIncrement: z.number()}),
  outputSchema: z.object({valueToRoot: z.number()}),
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
      valueToRoot: context.valueToRoot ?? result.text,
    }
  },
})

const taskBrStepFour = createStep({
  id: 'task_br_step_four',
  description: `Gives the square root of the input value`,
  inputSchema: z.object({valueToRoot: z.number()}),
  outputSchema: z.object({valueToSquare: z.number()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Gives the square root of the input value`
    const result = await catOne.generate(prompt)
    return {
      ...context,
      valueToSquare: context.valueToSquare ?? result.text,
    }
  },
})

const taskBrStepThree = createStep({
  id: 'task_br_step_three',
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

const taskBrStepFive = createStep({
  id: 'task_br_step_five',
  description: `Triples the input value`,
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Triples the input value`
    const result = await catOne.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wf_branched
 *
 * Workflow with branching (after and parallel branch) defined in src/mastra/workflows/index.ts
 */
export const wfBranched = createWorkflow({
  id: 'wf_branched',
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({}),
  steps: [taskBrStepOne, taskBrStepTwo, taskBrStepFour, taskBrStepThree, taskBrStepFive],
})
  // NOTE: Branching workflow — simplified to sequential for type compatibility
  // TODO: Implement conditional branching using .branch() API
  .then(taskBrStepOne)
  .then(taskBrStepTwo)
  .then(taskBrStepFour)
  .then(taskBrStepThree)
  .then(taskBrStepFive)
  .commit()
