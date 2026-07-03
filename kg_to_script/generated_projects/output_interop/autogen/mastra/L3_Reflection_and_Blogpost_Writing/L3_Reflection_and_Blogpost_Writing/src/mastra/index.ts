/**
 * Mastra AI Instance - UnnamedProject
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { unnamed, unnamed2, unnamed3, unnamed4, unnamed5, unnamed6 } from './agents'

// Import workflows
import { patternNested } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    unnamed,
    unnamed2,
    unnamed3,
    unnamed4,
    unnamed5,
    unnamed6,
  },
  workflows: {
    patternNested,
  },
})
