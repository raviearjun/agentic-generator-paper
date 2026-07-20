/**
 * Workflow: workflow_custom_crew
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow inferred from Crew(..., tasks=[task_1_name, task_2_name]) ordering.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { agent1Name, agent2Name } from '../agents'

// ── Workflow Steps ──

const task1 = createStep({
  id: 'task_1',
  description: `Do something as part of task 1`,
  inputSchema: z.object({var1: z.string(), var2: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Do something as part of task 1

If you do your BEST WORK, I'll give you a $10,000 commission!

Make sure to use the most recent data as possible.

Use this variable: ${context.var1 ?? ''}
And also this variable: ${context.var2 ?? ''}`
    const result = await agent1Name.generate(prompt)
    return { ...context, output: result.text }
  },
})

const task2 = createStep({
  id: 'task_2',
  description: `Take the input from task 1 and do something with it.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Take the input from task 1 and do something with it.

If you do your BEST WORK, I'll give you a $10,000 commission!

Make sure to do something else.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agent2Name.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_custom_crew
 *
 * Workflow inferred from Crew(..., tasks=[task_1_name, task_2_name]) ordering.
 */
export const workflowCustomCrew = createWorkflow({
  id: 'workflow_custom_crew',
  inputSchema: z.object({var1: z.string(), var2: z.string()}),
  outputSchema: z.object({}),
  steps: [task1, task2],
})
  .then(task1)
  .then(task2)
  .commit()
