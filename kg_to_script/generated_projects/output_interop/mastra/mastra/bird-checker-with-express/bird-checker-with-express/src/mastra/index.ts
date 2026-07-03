/**
 * Mastra AI Instance - BirdCheckerSystem
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Determine whether an image contains a bird, identify the species, and summarize the location.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { birdChecker } from './agents'

// Import workflows
import { birdCheckWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Mastra instance that hosts the bird checker agent and associated tools.
 */
export const mastra = new Mastra({
  agents: {
    birdChecker,
  },
  workflows: {
    birdCheckWorkflow,
  },
})
