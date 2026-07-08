/**
 * Workflow: wp_sequential
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Sequential Crew process as configured in crew.Crew(process=Process.sequential)
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { seniorEngineerAgent, qaEngineerAgent, chiefQaEngineerAgent } from '../agents'

// ── Workflow Steps ──

const taskCode = createStep({
  id: 'task_code',
  description: `You will create a game using python, these are the instructions:`,
  inputSchema: z.object({game: z.string()}),
  outputSchema: z.object({game: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You will create a game using python, these are the instructions:

Instructions
# ------------
${context.game ?? ''}`
    const result = await seniorEngineerAgent.generate(prompt)
    return {
      ...context,
      game: context.game ?? result.text,
    }
  },
})

const taskReview = createStep({
  id: 'task_review',
  description: `You will create a game using python, these are the instructions:`,
  inputSchema: z.object({game: z.string()}),
  outputSchema: z.object({game: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You will create a game using python, these are the instructions:

Instructions
# ------------
${context.game ?? ''}

Using the code you got, check for errors. Check for logic errors,
syntax errors, missing imports, variable declarations, mismatched brackets,
and security vulnerabilities.`
    const result = await qaEngineerAgent.generate(prompt)
    return {
      ...context,
      game: context.game ?? result.text,
    }
  },
})

const taskEvaluate = createStep({
  id: 'task_evaluate',
  description: `You are helping create a game using python, these are the instructions:`,
  inputSchema: z.object({game: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are helping create a game using python, these are the instructions:

Instructions
# ------------
${context.game ?? ''}

You will look over the code to insure that it is complete and
does the job that it is supposed to do.`
    const result = await chiefQaEngineerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wp_sequential
 *
 * Sequential Crew process as configured in crew.Crew(process=Process.sequential)
 */
export const wpSequential = createWorkflow({
  id: 'wp_sequential',
  inputSchema: z.object({game: z.string()}),
  outputSchema: z.object({}),
  steps: [taskCode, taskReview, taskEvaluate],
})
  .then(taskCode)
  .then(taskReview)
  .then(taskEvaluate)
  .commit()
