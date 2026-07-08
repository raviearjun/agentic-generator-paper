/**
 * Workflow: bird_check_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Simple workflow representing (1) obtaining an image and (2) analyzing it with the birdCheckerAgent.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { birdChecker } from '../agents'

// Import tools used by workflow steps
import { getRandomImageTool } from '../tools'

// ── Workflow Steps ──

const getRandomImageTask = createStep({
  id: 'get_random_image_task',
  description: `Fetch a random image from Unsplash matching the provided query parameter (wildlife | bird | feathers | flying). Return imageUrl, photographerName, and photographerProfile.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Fetch a random image from Unsplash matching the provided query parameter (wildlife | bird | feathers | flying). Return imageUrl, photographerName, and photographerProfile.
    // This step uses tool: getRandomImageTool
    // TODO: Implement step logic
    throw new Error('get_random_image_task not implemented yet')
  },
})

const imageMetadataTask = createStep({
  id: 'image_metadata_task',
  description: `View this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student.`,
  inputSchema: z.object({}),
  outputSchema: z.object({JSON_object_with_keys: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `View this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student.`
    const result = await birdChecker.generate(prompt)
    return {
      ...context,
      JSON_object_with_keys: context.JSON_object_with_keys ?? result.text,
    }
  },
})

// ── Workflow Definition ──

/**
 * bird_check_workflow
 *
 * Simple workflow representing (1) obtaining an image and (2) analyzing it with the birdCheckerAgent.
 */
export const birdCheckWorkflow = createWorkflow({
  id: 'bird_check_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({JSON_object_with_keys: z.string()}),
  steps: [getRandomImageTask, imageMetadataTask],
})
  .then(getRandomImageTask)
  .then(imageMetadataTask)
  .commit()
