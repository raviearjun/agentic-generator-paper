/**
 * Mastra AI Instance - Mastrainstance
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { catOne } from './agents'

// Import workflows
import { wfSequential, wfParallel, wfBranched, wfCyclical } from './workflows'

// Import memory instances
import { pgMemoryInstance } from './memory'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance configured in src/mastra/index.ts with one agent and four workflows.
 */
export const mastra = new Mastra({
  agents: {
    catOne,
  },
  workflows: {
    wfSequential,
    wfParallel,
    wfBranched,
    wfCyclical,
  },
  memory: {
    pgMemoryInstance,
  },
})
