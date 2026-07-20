/**
 * Workflow: workflow_sync_csv_data
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { travelAnalyzer } from '../agents'

// ── Workflow Steps ──

const taskSyncCsvData = createStep({
  id: 'task_sync_csv_data',
  description: `Sync data from City CSV (src/data/city-data.csv). Read CSV rows, map columns to CityData, and call mastra.engine.syncRecords to sync City records. This step is executed by the Mastra engine runtime.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Sync data from City CSV (src/data/city-data.csv). Read CSV rows, map columns to CityData, and call mastra.engine.syncRecords to sync City records. This step is executed by the Mastra engine runtime.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await travelAnalyzer.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_sync_csv_data
 */
export const workflowSyncCsvData = createWorkflow({
  id: 'workflow_sync_csv_data',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskSyncCsvData],
})
  .then(taskSyncCsvData)
  .commit()
