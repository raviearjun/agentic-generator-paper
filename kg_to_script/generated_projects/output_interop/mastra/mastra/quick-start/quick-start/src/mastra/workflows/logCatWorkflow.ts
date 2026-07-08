/**
 * Workflow: log_cat_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import tools used by workflow steps
import { mastraRuntime } from '../tools'

// ── Workflow Steps ──

const taskLogCatName = createStep({
  id: 'task_log_cat_name',
  description: `Log the cat name provided in the trigger: console.log(\`Hello, \${name} 🐈\`)`,
  inputSchema: z.object({name: z.string()}),
  outputSchema: z.object({name: z.string()}),
  execute: async ({ inputData }) => {
    // Log the cat name provided in the trigger: console.log(\`Hello, \${name} 🐈\`)
    // This step uses tool: mastraRuntime
    // TODO: Implement step logic
    throw new Error('task_log_cat_name not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * log_cat_workflow
 */
export const logCatWorkflow = createWorkflow({
  id: 'log_cat_workflow',
  inputSchema: z.object({name: z.string()}),
  outputSchema: z.object({name: z.string()}),
  steps: [taskLogCatName],
})
  .parallel([taskLogCatName])
  .commit()
