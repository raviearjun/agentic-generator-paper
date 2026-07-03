/**
 * Mastra AI Instance - Mastravnext
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { openapiSpecGenAgent } from './agents'

// Import workflows
import { wpOpenApiSpecGenWorkflow, wpMakePrToMastra } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance configured in src/mastra/index.ts (serviceName: mastra-vnext).
 */
export const mastra = new Mastra({
  agents: {
    openapiSpecGenAgent,
  },
  workflows: {
    wpOpenApiSpecGenWorkflow,
    wpMakePrToMastra,
  },
})
