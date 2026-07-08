/**
 * Workflow: wp_sequential
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { leadMarketAnalyst, chiefMarketingStrategist, creativeContentCreator } from '../agents'

// ── Workflow Steps ──

const taskResearch = createStep({
  id: 'task_research',
  description: `Conduct a thorough research about the customer and competitors in the context of {customer_domain}.`,
  inputSchema: z.object({customer_domain: z.string(), project_description: z.string()}),
  outputSchema: z.object({project_description: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct a thorough research about the customer and competitors in the context of ${context.customer_domain ?? ''}.
Make sure you find any interesting and relevant information given the current year is 2024.
We are working with them on the following project: ${context.project_description ?? ''}.`
    const result = await leadMarketAnalyst.generate(prompt)
    return {
      ...context,
      project_description: context.project_description ?? result.text,
    }
  },
})

const taskProjectUnderstanding = createStep({
  id: 'task_project_understanding',
  description: `Understand the project details and the target audience for {project_description}.`,
  inputSchema: z.object({project_description: z.string()}),
  outputSchema: z.object({project_description: z.string(), customer_domain: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Understand the project details and the target audience for ${context.project_description ?? ''}.
Review any provided materials and gather additional information as needed.`
    const result = await chiefMarketingStrategist.generate(prompt)
    return {
      ...context,
      project_description: context.project_description ?? result.text,
      customer_domain: context.customer_domain ?? result.text,
    }
  },
})

const taskMarketingStrategy = createStep({
  id: 'task_marketing_strategy',
  description: `Formulate a comprehensive marketing strategy for the project {project_description} of the customer {customer_domain}.`,
  inputSchema: z.object({project_description: z.string(), customer_domain: z.string()}),
  outputSchema: z.object({project_description: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Formulate a comprehensive marketing strategy for the project ${context.project_description ?? ''} of the customer ${context.customer_domain ?? ''}.
Use the insights from the research task and the project understanding task to create a high-quality strategy.`
    const result = await chiefMarketingStrategist.generate(prompt)
    return {
      ...context,
      project_description: context.project_description ?? result.text,
    }
  },
})

const taskCampaignIdea = createStep({
  id: 'task_campaign_idea',
  description: `Develop creative marketing campaign ideas for {project_description}.`,
  inputSchema: z.object({project_description: z.string()}),
  outputSchema: z.object({project_description: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Develop creative marketing campaign ideas for ${context.project_description ?? ''}.
Ensure the ideas are innovative, engaging, and aligned with the overall marketing strategy.`
    const result = await creativeContentCreator.generate(prompt)
    return {
      ...context,
      project_description: context.project_description ?? result.text,
    }
  },
})

const taskCopyCreation = createStep({
  id: 'task_copy_creation',
  description: `Create marketing copies based on the approved campaign ideas for {project_description}.`,
  inputSchema: z.object({project_description: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Create marketing copies based on the approved campaign ideas for ${context.project_description ?? ''}.
Ensure the copies are compelling, clear, and tailored to the target audience.`
    const result = await creativeContentCreator.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wp_sequential
 */
export const wpSequential = createWorkflow({
  id: 'wp_sequential',
  inputSchema: z.object({customer_domain: z.string(), project_description: z.string()}),
  outputSchema: z.object({}),
  steps: [taskResearch, taskProjectUnderstanding, taskMarketingStrategy, taskCampaignIdea, taskCopyCreation],
})
  .then(taskResearch)
  .then(taskProjectUnderstanding)
  .then(taskMarketingStrategy)
  .then(taskCampaignIdea)
  .then(taskCopyCreation)
  .commit()
