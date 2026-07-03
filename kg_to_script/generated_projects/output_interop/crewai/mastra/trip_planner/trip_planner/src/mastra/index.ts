/**
 * Mastra AI Instance - TripPlannerCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Select the best city based on weather, season, and prices
 *   - : Provide the BEST insights about the selected city
 *   - : Create the most amazing travel itineraries with budget and packing suggestions for the city
 *   - : Automate the process of choosing among city options and producing a full trip itinerary based on traveler preferences.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { citySelectionAgent, localExpertAgent, travelConciergeAgent } from './agents'

// Import workflows
import { patternTripPlanning } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * CrewAI-based team that coordinates city selection, local research, and itinerary planning.
 */
export const mastra = new Mastra({
  agents: {
    citySelectionAgent,
    localExpertAgent,
    travelConciergeAgent,
  },
  workflows: {
    patternTripPlanning,
  },
})
