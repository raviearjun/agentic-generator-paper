/**
 * Workflow: workflow_copy_crew
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { productCompetitorAgent, strategyPlannerAgent, creativeContentCreatorAgent } from '../agents'

// ── Workflow Steps ──

const taskProductAnalysis = createStep({
  id: 'task_product_analysis',
  description: `Analyze the given product website: {product_website}.`,
  inputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Analyze the given product website: ${context.product_website ?? ''}.
Extra details provided by the customer: ${context.product_details ?? ''}.
Focus on identifying unique features, benefits, and the overall narrative. Provide a final report articulating key selling points, market appeal, and suggestions for enhancement or positioning. Attention to detail and up-to-date (2024) context required.`
    const result = await productCompetitorAgent.generate(prompt)
    return {
      ...context,
      product_website: context.product_website ?? result.text,
      product_details: context.product_details ?? result.text,
    }
  },
})

const taskCompetitorAnalysis = createStep({
  id: 'task_competitor_analysis',
  description: `Explore competitors of: {product_website}.`,
  inputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Explore competitors of: ${context.product_website ?? ''}.
Extra details provided by the customer: ${context.product_details ?? ''}.
Identify the top 3 competitors and analyze their strategies, market positioning, and customer perception. Include context about the target website and detailed comparison.`
    const result = await productCompetitorAgent.generate(prompt)
    return {
      ...context,
      product_website: context.product_website ?? result.text,
      product_details: context.product_details ?? result.text,
    }
  },
})

const taskCampaignDevelopment = createStep({
  id: 'task_campaign_development',
  description: `Create a targeted marketing campaign for: {product_website}.`,
  inputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Create a targeted marketing campaign for: ${context.product_website ?? ''}.
Extra details provided by the customer: ${context.product_details ?? ''}.
Produce strategy and creative content ideas designed to captivate the target audience. Provide ideas that resonate with the audience and include all available product/context information.`
    const result = await strategyPlannerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskInstagramAdCopy = createStep({
  id: 'task_instagram_ad_copy',
  description: `Craft an engaging Instagram post copy. The copy should be punchy, captivating, concise, and aligned with the product marketing strategy. Focus on creating a message that resonates with the target audience and highlights the product's unique selling points.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Craft an engaging Instagram post copy. The copy should be punchy, captivating, concise, and aligned with the product marketing strategy. Focus on creating a message that resonates with the target audience and highlights the product's unique selling points.`
    const result = await creativeContentCreatorAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_copy_crew
 */
export const workflowCopyCrew = createWorkflow({
  id: 'workflow_copy_crew',
  inputSchema: z.object({product_website: z.string(), product_details: z.string()}),
  outputSchema: z.object({}),
  steps: [taskProductAnalysis, taskCompetitorAnalysis, taskCampaignDevelopment, taskInstagramAdCopy],
})
  .then(taskProductAnalysis)
  .then(taskCompetitorAnalysis)
  .then(taskCampaignDevelopment)
  .then(taskInstagramAdCopy)
  .commit()
