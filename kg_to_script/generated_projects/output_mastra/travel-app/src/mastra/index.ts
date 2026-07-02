/**
 * Mastra AI Instance - MastraInstance
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { travelAgent, travelAnalyzer } from './agents'

// Import workflows
import { workflowTravelSubmission, workflowSyncCsvData } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    travelAgent,
    travelAnalyzer,
  },
  workflows: {
    workflowTravelSubmission,
    workflowSyncCsvData,
  },
})
