/**
 * Mastra AI Instance - Mastrainstance
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { mastraAgent } from './agents'

// Import workflows
import { myWorkflowPattern } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    mastraAgent,
  },
  workflows: {
    myWorkflowPattern,
  },
})
