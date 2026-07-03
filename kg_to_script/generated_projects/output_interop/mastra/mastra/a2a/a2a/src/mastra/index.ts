/**
 * Mastra AI Instance - MastraA2AClient
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { agentIdConstructorParameter } from './agents'

// Import workflows
import { a2AClientWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Represents the client-side component that orchestrates A2A interactions with a remote agent.
 */
export const mastra = new Mastra({
  agents: {
    agentIdConstructorParameter,
  },
  workflows: {
    a2AClientWorkflow,
  },
})
