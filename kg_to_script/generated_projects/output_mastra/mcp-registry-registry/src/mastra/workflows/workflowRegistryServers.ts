/**
 * Workflow: workflow_registry_servers
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Inferred workflow for serving registry server listing: start -> fetch & post-process -> filter -> return results.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { registryRegistryServer } from '../agents'

// ── Workflow Steps ──

const taskFetchServersFromRegistry = createStep({
  id: 'task_fetch_servers_from_registry',
  description: `Fetch servers from the registry by locating the registry entry in local registryData, verifying servers_url, performing HTTP GET, and returning raw response for post-processing.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Fetch servers from the registry by locating the registry entry in local registryData, verifying servers_url, performing HTTP GET, and returning raw response for post-processing.`
    const result = await registryRegistryServer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskPostProcessServers = createStep({
  id: 'task_post_process_servers',
  description: `Normalize registry-specific response formats into canonical ServerEntry objects with id, name, description, createdAt, updatedAt using the registry's postProcessServers function when available.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Normalize registry-specific response formats into canonical ServerEntry objects with id, name, description, createdAt, updatedAt using the registry's postProcessServers function when available.`
    const result = await registryRegistryServer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskFilterServers = createStep({
  id: 'task_filter_servers',
  description: `Apply search filtering on server name or description; support tag-based filtering when server metadata includes tags.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Apply search filtering on server name or description; support tag-based filtering when server metadata includes tags.`
    const result = await registryRegistryServer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGetServersFromRegistry = createStep({
  id: 'task_get_servers_from_registry',
  description: `Orchestrate fetching, post-processing, and filtering of servers for a given registryId and optional filters; return final server list or throw on error.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Orchestrate fetching, post-processing, and filtering of servers for a given registryId and optional filters; return final server list or throw on error.`
    const result = await registryRegistryServer.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_registry_servers
 *
 * Inferred workflow for serving registry server listing: start -> fetch & post-process -> filter -> return results.
 */
export const workflowRegistryServers = createWorkflow({
  id: 'workflow_registry_servers',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskFetchServersFromRegistry, taskPostProcessServers, taskFilterServers, taskGetServersFromRegistry],
})
  .then(taskFetchServersFromRegistry)
  .then(taskPostProcessServers)
  .then(taskFilterServers)
  .then(taskGetServersFromRegistry)
  .commit()
