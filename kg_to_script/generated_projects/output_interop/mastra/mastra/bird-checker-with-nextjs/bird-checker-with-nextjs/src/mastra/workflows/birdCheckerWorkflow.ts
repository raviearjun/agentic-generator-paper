/**
 * Workflow: bird_checker_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
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
  description: `Fetch a random image from Unsplash matching the provided query (wildlife | feathers | flying | birds).`,
  inputSchema: z.object({query: z.string()}),
  outputSchema: z.object({image: z.string()}),
  execute: async ({ inputData }) => {
    // Fetch a random image from Unsplash matching the provided query (wildlife | feathers | flying | birds).
    // This step uses tool: getRandomImageTool
    // TODO: Implement step logic
    throw new Error('get_image_task not implemented yet')
  },
})

const birdCheckTask = createStep({
  id: 'bird_check_task',
  description: `view this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student`,
  inputSchema: z.object({image: z.string()}),
  outputSchema: z.object({bird: z.boolean()}),
  execute: async ({ inputData }) => {
    // view this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student
    // This step uses agent: birdAgent
    // const result = await birdAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('bird_check_task not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * bird_checker_workflow
 */
export const birdCheckerWorkflow = createWorkflow({
  id: 'bird_checker_workflow',
  inputSchema: z.object({query: z.string()}),
  outputSchema: z.object({bird: z.boolean()}),
  steps: [getImageTask, birdCheckTask],
})
  .then(getImageTask)
  .then(birdCheckTask)
  .commit()
