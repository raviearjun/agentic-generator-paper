/**
 * Mastra AI Instance - GameBuilderCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Create software as needed
 *   - : Create Perfect code, by analyzing the code that is given for errors
 *   - : Ensure that the code does the job that it is supposed to do
 *   - : Automate the creation of a Python-based game using autonomous agents orchestrated by the CrewAI framework.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { seniorEngineerAgent, qaEngineerAgent, chiefQaEngineerAgent } from './agents'

// Import workflows
import { wpSequential } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * CrewAI crew defined in GameBuilderCrew class (src/game_builder_crew/crew.py)
 */
export const mastra = new Mastra({
  agents: {
    seniorEngineerAgent,
    qaEngineerAgent,
    chiefQaEngineerAgent,
  },
  workflows: {
    wpSequential,
  },
})
