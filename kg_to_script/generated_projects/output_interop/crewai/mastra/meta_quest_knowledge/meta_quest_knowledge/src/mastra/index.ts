/**
 * Mastra AI Instance - MetaQuestKnowledgeCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Agent-level goal extracted from agents.yaml.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { metaQuestExpert } from './agents'

// Import workflows
import { sequentialPattern } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    metaQuestExpert,
  },
  workflows: {
    sequentialPattern,
  },
})
