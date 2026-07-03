/**
 * Mastra AI Instance - CustomCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Define agent 1 goal here
 *   - : Define agent 2 goal here
 */

import { Mastra } from '@mastra/core'

// Import agents
import { agent1Name, agent2Name } from './agents'

// Import workflows
import { workflowCustomCrew } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Crew created in main.CustomCrew with agents [custom_agent_1, custom_agent_2] and tasks [custom_task_1, custom_task_2].
 */
export const mastra = new Mastra({
  agents: {
    agent1Name,
    agent2Name,
  },
  workflows: {
    workflowCustomCrew,
  },
})
