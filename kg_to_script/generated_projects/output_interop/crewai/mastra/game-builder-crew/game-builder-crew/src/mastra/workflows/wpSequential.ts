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
  description: `code_task from config/tasks.yaml`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // You will create a game using python, these are the instructions:
    // This step uses agent: seniorEngineerAgent
    // const result = await seniorEngineerAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_code not implemented yet')
  },
})

const taskReview = createStep({
  id: 'task_review',
  description: `review_task from config/tasks.yaml`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // You will create a game using python, these are the instructions:
    // This step uses agent: qaEngineerAgent
    // const result = await qaEngineerAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_review not implemented yet')
  },
})

const taskEvaluate = createStep({
  id: 'task_evaluate',
  description: `evaluate_task from config/tasks.yaml`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // You are helping create a game using python, these are the instructions:
    // This step uses agent: chiefQaEngineerAgent
    // const result = await chiefQaEngineerAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_evaluate not implemented yet')
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
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskCode, taskReview, taskEvaluate],
})
  .then(taskCode)
  .then(taskReview)
  .then(taskEvaluate)
  .commit()
