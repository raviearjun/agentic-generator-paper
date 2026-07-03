/**
 * Mastra AI Instance - SurpriseTravelCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Create a comprehensive surprise travel plan for the traveler covering activities, restaurants, and a day-by-day itinerary.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { personalizedActivityPlanner, restaurantScout, itineraryCompiler } from './agents'

// Import workflows
import { workflowSequential } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    personalizedActivityPlanner,
    restaurantScout,
    itineraryCompiler,
  },
  workflows: {
    workflowSequential,
  },
})
