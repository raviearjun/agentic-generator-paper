/**
 * Workflow: bird_checker_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Inferred two-step workflow: fetch an image, then classify it.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { birdAgent } from '../agents'

// Import tools used by workflow steps
import { getRandomImageTool } from '../tools'

// ── Workflow Steps ──

const getImageTask = createStep({
  id: 'get_image_task',
  description: `UI-triggered task to obtain a random image from Unsplash based on selected query.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Get a random image from Unsplash based on the selected option (wildlife, feathers, flying, birds).
    // This step uses tool: getRandomImageTool
    // TODO: Implement step logic
    throw new Error('get_image_task not implemented yet')
  },
})

const classifyImageTask = createStep({
  id: 'classify_image_task',
  description: `Agent task to determine bird presence, species, and summarize location.`,
  inputSchema: z.object({}),
  outputSchema: z.object({Object_with_fields: z.string()}),
  execute: async ({ inputData }) => {
    // view this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student
    // This step uses agent: birdAgent
    // const result = await birdAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('classify_image_task not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * bird_checker_workflow
 *
 * Inferred two-step workflow: fetch an image, then classify it.
 */
export const birdCheckerWorkflow = createWorkflow({
  id: 'bird_checker_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({Object_with_fields: z.string()}),
  steps: [getImageTask, classifyImageTask],
})
  .then(getImageTask)
  .then(classifyImageTask)
  .commit()
