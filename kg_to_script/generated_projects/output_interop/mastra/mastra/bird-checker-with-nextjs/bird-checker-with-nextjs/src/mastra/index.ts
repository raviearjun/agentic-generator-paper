/**
 * Mastra AI Instance - BirdCheckerSystem
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Identify if an image depicts a bird, provide the scientific name if it is a bird, and summarize the image location in one or two short sentences.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { birdAgent } from './agents'

// Import workflows
import { birdCheckerWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    birdAgent,
  },
  workflows: {
    birdCheckerWorkflow,
  },
})
