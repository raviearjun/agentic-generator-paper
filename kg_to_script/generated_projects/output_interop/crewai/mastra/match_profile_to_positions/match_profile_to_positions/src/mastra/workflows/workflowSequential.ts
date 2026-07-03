/**
 * Workflow: workflow_sequential
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Sequential workflow pattern corresponding to Crew Process.sequential with two steps: read CV then match CV.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { cvReader, matcher } from '../agents'

// ── Workflow Steps ──

const taskReadCv = createStep({
  id: 'task_read_cv',
  description: `Extract relevant information from the given CV: professional summary, technical skills, work history, education, key achievements.`,
  inputSchema: z.object({path_to_cv: z.string()}),
  outputSchema: z.object({path_to_jobs_csv: z.string(), path_to_cv: z.string()}),
  execute: async ({ inputData }) => {
    // Extract relevant information from the given CV. Focus on skills, experience, education, and key achievements.
    // This step uses agent: cvReader
    // const result = await cvReader.generate('...')
    // TODO: Implement step logic
    throw new Error('task_read_cv not implemented yet')
  },
})

const taskMatchCv = createStep({
  id: 'task_match_cv',
  description: `Match the CV to the job opportunities based on skills, experience, and key achievements; produce a ranked list.`,
  inputSchema: z.object({path_to_jobs_csv: z.string(), path_to_cv: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Match the CV to the job opportunities based on skills, experience, and key achievements.
    // This step uses agent: matcher
    // const result = await matcher.generate('...')
    // TODO: Implement step logic
    throw new Error('task_match_cv not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * workflow_sequential
 *
 * Sequential workflow pattern corresponding to Crew Process.sequential with two steps: read CV then match CV.
 */
export const workflowSequential = createWorkflow({
  id: 'workflow_sequential',
  inputSchema: z.object({path_to_cv: z.string()}),
  outputSchema: z.object({}),
  steps: [taskReadCv, taskMatchCv],
})
  .then(taskReadCv)
  .then(taskMatchCv)
  .commit()
