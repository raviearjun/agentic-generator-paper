/**
 * Mastra AI Instance - BirdCheckerSystem
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : System should determine whether a provided image contains a bird, identify its scientific name if present, and summarize location.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { birdAgent } from './agents'

// Import workflows
import { birdCheckerWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance wrapping the birdAgent and application workflow.
 */
export const mastra = new Mastra({
  agents: {
    birdAgent,
  },
  workflows: {
    birdCheckerWorkflow,
  },
})
