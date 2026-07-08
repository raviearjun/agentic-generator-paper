/**
 * Workflow: workflow_image_crew
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { seniorPhotographerAgent, chiefCreativeDiretorAgent } from '../agents'

// ── Workflow Steps ──

const taskTakePhotograph = createStep({
  id: 'task_take_photograph',
  description: `You MUST take the most amazing photo ever for an instagram post regarding the product. Provided ad copy: {copy}`,
  inputSchema: z.object({copy: z.string(), product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You MUST take the most amazing photo ever for an instagram post regarding the product. Provided ad copy: ${context.copy ?? ''}
Product: ${context.product_website ?? ''}
Extra details: ${context.product_details ?? ''}
Imagine the photograph and describe it in a paragraph. Follow examples (professional wide shot, soft lighting, 4k, crisp, etc.). Do not show the actual product in photos.`
    const result = await seniorPhotographerAgent.generate(prompt)
    return {
      ...context,
      product_website: context.product_website ?? result.text,
      product_details: context.product_details ?? result.text,
    }
  },
})

const taskReviewPhoto = createStep({
  id: 'task_review_photo',
  description: `Review the photos from the senior photographer. Ensure alignment with product goals; review, approve, ask clarifying questions or delegate follow-up work as necessary. When delegating, include the full draft as part of the information.`,
  inputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Review the photos from the senior photographer. Ensure alignment with product goals; review, approve, ask clarifying questions or delegate follow-up work as necessary. When delegating, include the full draft as part of the information.
Product: ${context.product_website ?? ''}
Extra details: ${context.product_details ?? ''}
Examples: (high tech airplane in a beautiful blue sky ...; the last supper ...; a bearded old man in the snows ...).`
    const result = await chiefCreativeDiretorAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_image_crew
 */
export const workflowImageCrew = createWorkflow({
  id: 'workflow_image_crew',
  inputSchema: z.object({copy: z.string(), product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({}),
  steps: [taskTakePhotograph, taskReviewPhoto],
})
  .then(taskTakePhotograph)
  .then(taskReviewPhoto)
  .commit()
