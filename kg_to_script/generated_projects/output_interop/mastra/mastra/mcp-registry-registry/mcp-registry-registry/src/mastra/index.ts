/**
 * Mastra AI Instance - RegistryRegistryMcpServer
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Provide discovery and access to MCP registries and their servers; normalize heterogeneous registry responses into a standard ServerEntry format.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { registryRegistryServer } from './agents'

// Import workflows
import { workflowRegistryServers } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * An MCP server that provides a registry of MCP registries and exposes tools 'registryList' and 'registryServers'.
 */
export const mastra = new Mastra({
  agents: {
    registryRegistryServer,
  },
  workflows: {
    workflowRegistryServers,
  },
})
