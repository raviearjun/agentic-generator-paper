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
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Analyse in much detail the following discussion: ### DISCUSSION: {{discussion}}
    // This step uses agent: analyst
    // const result = await analyst.generate('...')
    // TODO: Implement step logic
    throw new Error('task1 not implemented yet')
  },
})

const task2 = createStep({
  id: 'task2',
  description: `Create a dialogue heavy screenplay from the discussion, between two persons. Do NOT write parentheticals. Leave out wrylies. You MUST SKIP directional notes.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Create a dialogue heavy screenplay from the discussion, between two persons. Do NOT write parentheticals. Leave out wrylies. You MUST SKIP directional notes.
    // This step uses agent: scriptwriter
    // const result = await scriptwriter.generate('...')
    // TODO: Implement step logic
    throw new Error('task2 not implemented yet')
  },
})

const task3 = createStep({
  id: 'task3',
  description: `Format the script exactly like this:   ## (person 1): (first text line from person 1) ...`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Format the script exactly like this:   ## (person 1): (first text line from person 1)    ## (person 2): (first text line from person 2) ...
    // This step uses agent: formatter
    // const result = await formatter.generate('...')
    // TODO: Implement step logic
    throw new Error('task3 not implemented yet')
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
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [task1, task2, task3],
})
  .then(task1)
  .then(task2)
  .then(task3)
  .commit()
