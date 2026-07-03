/**
 * Mastra AI Instance - TripPlannerAppTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { tripPlannerAgent } from './agents'

// Import workflows
import { tripPlannerWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Team representing the LangGraph-backed trip planner UI and backend flows.
 */
export const mastra = new Mastra({
  agents: {
    tripPlannerAgent,
  },
  workflows: {
    tripPlannerWorkflow,
  },
})
