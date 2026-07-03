/**
 * Mastra AI Instance - StandupDuo
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Deliver a short comedic routine for the audience.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { chatbot, unnamed, unnamed2 } from './agents'

// Import workflows
import { workflowXiangsheng } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    chatbot,
    unnamed,
    unnamed2,
  },
  workflows: {
    workflowXiangsheng,
  },
})
