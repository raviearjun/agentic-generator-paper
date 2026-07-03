/**
 * Mastra AI Instance - EmailAssistantTeamStateGraphsystem
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Human Agents:
 *   - human_user ()
 */

import { Mastra } from '@mastra/core'

// Import agents
import { emailAssistantAgent } from './agents'

// Import workflows
import { emailAgentStateGraph } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    emailAssistantAgent,
  },
  workflows: {
    emailAgentStateGraph,
  },
})
