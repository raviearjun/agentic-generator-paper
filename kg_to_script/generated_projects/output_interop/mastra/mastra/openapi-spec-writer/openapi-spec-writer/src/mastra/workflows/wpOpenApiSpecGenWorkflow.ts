/**
 * Workflow: wp_open_api_spec_gen_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow to crawl a site, generate OpenAPI fragments per page, then merge into a single spec.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { openapiSpecGenAgent } from '../agents'

// Import tools used by workflow steps
import { toolSiteCrawl, toolGenerateSpec } from '../tools'

// ── Workflow Steps ──

const taskSiteCrawlSync = createStep({
  id: 'task_site_crawl_sync',
  description: `Crawl the provided URL, extract main content as markdown, include sourceURL in metadata. Use provided pathRegex and limit. Exclude nav/header/footer and unrelated tags; return markdown blocks and metadata.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Crawl the provided URL, extract main content as markdown, include sourceURL in metadata. Use provided pathRegex and limit. Exclude nav/header/footer and unrelated tags; return markdown blocks and metadata.
    // This step uses tool: toolSiteCrawl
    // TODO: Implement step logic
    throw new Error('task_site_crawl_sync not implemented yet')
  },
})

const taskGenerateSpec = createStep({
  id: 'task_generate_spec',
  description: `I have generated the following Open API specs: <list of fragments>. Merge them into a single spec and ensure the result is a valid OpenAPI YAML document. Remove code fences and unify components/paths to avoid duplicates.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `I have generated the following Open API specs: <list of fragments>. Merge them into a single spec and ensure the result is a valid OpenAPI YAML document. Remove code fences and unify components/paths to avoid duplicates.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await openapiSpecGenAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wp_open_api_spec_gen_workflow
 *
 * Workflow to crawl a site, generate OpenAPI fragments per page, then merge into a single spec.
 */
export const wpOpenApiSpecGenWorkflow = createWorkflow({
  id: 'wp_open_api_spec_gen_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskSiteCrawlSync, taskGenerateSpec],
})
  .then(taskSiteCrawlSync)
  .then(taskGenerateSpec)
  .commit()
