/**
 * Workflow: wf_sequential
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow defined in src/mastra/workflows/index.ts (sequential)
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { catOne } from '../agents'

// ── Workflow Steps ──

const taskStepOne = createStep({
  id: 'task_step_one',
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

const taskStepTwo = createStep({
  id: 'task_step_two',
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

const taskStepThree = createStep({
  id: 'task_step_three',
  description: `Squares the input value`,
  inputSchema: z.object({valueToSquare: z.number()}),
  outputSchema: z.object({valueToRoot: z.number()}),
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
      valueToRoot: context.valueToRoot ?? result.text,
    }
  },
})

const taskStepFour = createStep({
  id: 'task_step_four',
  description: `Gives the square root of the input value`,
  inputSchema: z.object({valueToRoot: z.number()}),
  outputSchema: z.object({inputValue: z.number()}),
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
      inputValue: context.inputValue ?? result.text,
    }
  },
})

const taskStepFive = createStep({
  id: 'task_step_five',
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
 * wf_sequential
 *
 * Workflow defined in src/mastra/workflows/index.ts (sequential)
 */
export const wfSequential = createWorkflow({
  id: 'wf_sequential',
  inputSchema: z.object({inputValue: z.number()}),
  outputSchema: z.object({}),
  steps: [taskStepOne, taskStepTwo, taskStepThree, taskStepFour, taskStepFive],
})
  // NOTE: Branching workflow — simplified to sequential for type compatibility
  // TODO: Implement conditional branching using .branch() API
  .then(taskStepOne)
  .then(taskStepTwo)
  .then(taskStepThree)
  .then(taskStepFour)
  .then(taskStepFive)
  .commit()
