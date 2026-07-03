/**
 * Mastra AI Instance - WriterStateGraphTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { writerAgent } from './agents'

// Import workflows
import { writerStateGraphPattern } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    writerAgent,
  },
  workflows: {
    writerStateGraphPattern,
  },
})
