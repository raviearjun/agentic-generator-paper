/**
 * Mastra AI Instance - Mastraruntime
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { mastraDefaultAgent } from './agents'

// Import workflows
import { myWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance created in src/mastra/index.ts with registered workflows.
 */
export const mastra = new Mastra({
  agents: {
    mastraDefaultAgent,
  },
  workflows: {
    myWorkflow,
  },
})
