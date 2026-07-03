/**
 * Mastra AI Instance - MastraInstancelocal
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { chefAgent } from './agents'

// Import workflows
import { chefWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance created in src/mastra/index.ts containing Chef Agent
 */
export const mastra = new Mastra({
  agents: {
    chefAgent,
  },
  workflows: {
    chefWorkflow,
  },
})
