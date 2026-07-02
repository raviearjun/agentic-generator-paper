/**
 * Mastra AI Instance - Mastrainstanceworkflowairecruiter
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { mastraLlm } from './agents'

// Import workflows
import { candidateWorkflowPattern } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance hosting the candidate-workflow
 */
export const mastra = new Mastra({
  agents: {
    mastraLlm,
  },
  workflows: {
    candidateWorkflowPattern,
  },
})
