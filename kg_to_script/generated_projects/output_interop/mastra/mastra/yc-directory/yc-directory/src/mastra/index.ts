/**
 * Mastra AI Instance - MastraInstanceycagent
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { ycDirectoryAgent } from './agents'

// Import workflows
import { ycDirectoryWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance constructed in src/mastra/index.ts with a single agent 'ycAgent' and logger configuration.
 */
export const mastra = new Mastra({
  agents: {
    ycDirectoryAgent,
  },
  workflows: {
    ycDirectoryWorkflow,
  },
})
