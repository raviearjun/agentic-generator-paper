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
  description: `Extract relevant information from the given CV. Focus on skills, experience, education, and key achievements.`,
  inputSchema: z.object({path_to_cv: z.string()}),
  outputSchema: z.object({path_to_jobs_csv: z.string(), path_to_cv: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Extract relevant information from the given CV. Focus on skills, experience, education, and key achievements.
Ensure to capture the candidate's professional summary, technical skills, work history, and educational background.

CV file: ${context.path_to_cv ?? ''}`
    const result = await cvReader.generate(prompt)
    return {
      ...context,
      path_to_jobs_csv: context.path_to_jobs_csv ?? result.text,
      path_to_cv: context.path_to_cv ?? result.text,
    }
  },
})

const taskMatchCv = createStep({
  id: 'task_match_cv',
  description: `Match the CV to the job opportunities based on skills, experience, and key achievements.`,
  inputSchema: z.object({path_to_jobs_csv: z.string(), path_to_cv: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Match the CV to the job opportunities based on skills, experience, and key achievements.
Evaluate how well the candidate's profile fits each job description, focusing on the alignment of skills, work history, and key achievements with the job requirements.

Jobs CSV file: ${context.path_to_jobs_csv ?? ''}

CV file: ${context.path_to_cv ?? ''}`
    const result = await matcher.generate(prompt)
    return { ...context, output: result.text }
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
