/**
 * Workflow: crew_sequential_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Sequential process executing tasks in order: analysis -> scriptwriting -> formatting.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { analyst, scriptwriter, formatter } from '../agents'

// ── Workflow Steps ──

const task1 = createStep({
  id: 'task1',
  description: `Analyse in much detail the following discussion: ### DISCUSSION: {{discussion}}`,
  inputSchema: z.object({discussion: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Analyse in much detail the following discussion: ### DISCUSSION: {${context.discussion ?? ''}}`
    const result = await analyst.generate(prompt)
    return { ...context, output: result.text }
  },
})

const task2 = createStep({
  id: 'task2',
  description: `Create a dialogue heavy screenplay from the discussion, between two persons. Do NOT write parentheticals. Leave out wrylies. You MUST SKIP directional notes.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Create a dialogue heavy screenplay from the discussion, between two persons. Do NOT write parentheticals. Leave out wrylies. You MUST SKIP directional notes.`
    const result = await scriptwriter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const task3 = createStep({
  id: 'task3',
  description: `Format the script exactly like this:   ## (person 1): (first text line from person 1)    ## (person 2): (first text line from person 2) ...`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Format the script exactly like this:   ## (person 1): (first text line from person 1)    ## (person 2): (first text line from person 2) ...`
    const result = await formatter.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * crew_sequential_workflow
 *
 * Sequential process executing tasks in order: analysis -> scriptwriting -> formatting.
 */
export const crewSequentialWorkflow = createWorkflow({
  id: 'crew_sequential_workflow',
  inputSchema: z.object({discussion: z.string()}),
  outputSchema: z.object({}),
  steps: [task1, task2, task3],
})
  .then(task1)
  .then(task2)
  .then(task3)
  .commit()
