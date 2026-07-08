/**
 * Workflow: yc_directory_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Simple workflow: Start -> Fetch directory -> Process results.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { ycDirectoryAgent } from '../agents'

// ── Workflow Steps ──

const fetchYcDirectoryTask = createStep({
  id: 'fetch_yc_directory_task',
  description: `Invoke the 'yc-directory' tool to retrieve the full 2024 YC directory. Return the array of company objects exactly as provided by the tool.`,
  inputSchema: z.object({yc: z.string()}),
  outputSchema: z.object({Format_the_retrieved_YC_directory_data_for_user: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Invoke the 'yc-directory' tool to retrieve the full 2024 YC directory. Return the array of company objects exactly as provided by the tool.`
    const result = await ycDirectoryAgent.generate(prompt)
    return {
      ...context,
      Format_the_retrieved_YC_directory_data_for_user: context.Format_the_retrieved_YC_directory_data_for_user ?? result.text,
    }
  },
})

const processYcDataTask = createStep({
  id: 'process_yc_data_task',
  description: `Format the retrieved YC directory data for user-friendly responses. Ensure each company mentions its batch and includes name, industries, and short summary.`,
  inputSchema: z.object({Format_the_retrieved_YC_directory_data_for_user: z.string()}),
  outputSchema: z.object({and_a_one: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Format the retrieved YC directory data for user-friendly responses. Ensure each company mentions its batch and includes name, industries, and short summary.`
    const result = await ycDirectoryAgent.generate(prompt)
    return {
      ...context,
      and_a_one: context.and_a_one ?? result.text,
    }
  },
})

// ── Workflow Definition ──

/**
 * yc_directory_workflow
 *
 * Simple workflow: Start -> Fetch directory -> Process results.
 */
export const ycDirectoryWorkflow = createWorkflow({
  id: 'yc_directory_workflow',
  inputSchema: z.object({yc: z.string()}),
  outputSchema: z.object({and_a_one: z.string()}),
  steps: [fetchYcDirectoryTask, processYcDataTask],
})
  .then(fetchYcDirectoryTask)
  .then(processYcDataTask)
  .commit()
