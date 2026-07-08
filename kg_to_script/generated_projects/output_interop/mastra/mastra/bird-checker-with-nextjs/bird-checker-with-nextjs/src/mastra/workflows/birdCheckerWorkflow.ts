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
  inputSchema: z.object({}),
  outputSchema: z.object({}),
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
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `view this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student`
    const result = await birdAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * bird_checker_workflow
 */
export const birdCheckerWorkflow = createWorkflow({
  id: 'bird_checker_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [getImageTask, birdCheckTask],
})
  .then(getImageTask)
  .then(birdCheckTask)
  .commit()
