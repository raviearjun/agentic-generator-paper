/**
 * Mastra AI Instance - StateGraphTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { chatAgent } from './agents'

// Import workflows
import { wpStategraph } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    chatAgent,
  },
  workflows: {
    wpStategraph,
  },
})
