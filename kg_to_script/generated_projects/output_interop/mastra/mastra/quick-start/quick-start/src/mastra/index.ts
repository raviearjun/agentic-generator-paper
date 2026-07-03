/**
 * Mastra AI Instance - Mastrainstance
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : No explicit goal provided in source; placeholder goal.
 *   - : No explicit goal provided in source; placeholder goal.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { catOne, agentTwo } from './agents'

// Import workflows
import { logCatWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    catOne,
    agentTwo,
  },
  workflows: {
    logCatWorkflow,
  },
})
