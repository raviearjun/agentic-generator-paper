/**
 * Workflow: workflow_blog_crew
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { biomedicalMarketingAgent, healthcareMarketingAgent, financialMarketingAgent } from '../agents'

// ── Workflow Steps ──

const taskBiomedicalResearch = createStep({
  id: 'task_biomedical_research',
  description: `Conduct a thorough research about {weaviate_feature}`,
  inputSchema: z.object({weaviate_feature: z.string()}),
  outputSchema: z.object({weaviate_feature: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct a thorough research about ${context.weaviate_feature ?? ''}
Make sure you find any interesting and relevant information using the web and Weaviate blogs.`
    const result = await biomedicalMarketingAgent.generate(prompt)
    return {
      ...context,
      weaviate_feature: context.weaviate_feature ?? result.text,
    }
  },
})

const taskHealthcareResearch = createStep({
  id: 'task_healthcare_research',
  description: `Conduct a thorough research about {weaviate_feature}`,
  inputSchema: z.object({weaviate_feature: z.string()}),
  outputSchema: z.object({weaviate_feature: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct a thorough research about ${context.weaviate_feature ?? ''}
Make sure you find any interesting and relevant information using the web and Weaviate blogs.`
    const result = await healthcareMarketingAgent.generate(prompt)
    return {
      ...context,
      weaviate_feature: context.weaviate_feature ?? result.text,
    }
  },
})

const taskFinancialResearch = createStep({
  id: 'task_financial_research',
  description: `Conduct a thorough research about {weaviate_feature}`,
  inputSchema: z.object({weaviate_feature: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct a thorough research about ${context.weaviate_feature ?? ''}
Make sure you find any interesting and relevant information using the web and Weaviate blogs.`
    const result = await financialMarketingAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_blog_crew
 */
export const workflowBlogCrew = createWorkflow({
  id: 'workflow_blog_crew',
  inputSchema: z.object({weaviate_feature: z.string()}),
  outputSchema: z.object({}),
  steps: [taskBiomedicalResearch, taskHealthcareResearch, taskFinancialResearch],
})
  .then(taskBiomedicalResearch)
  .then(taskHealthcareResearch)
  .then(taskFinancialResearch)
  .commit()
