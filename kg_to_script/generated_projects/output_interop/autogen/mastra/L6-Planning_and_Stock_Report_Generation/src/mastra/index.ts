/**
 * Mastra AI Instance - GroupChatTeamforBlogGeneration
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { admin, planner, engineer, executor, writer, groupChatManager } from './agents'

// Import workflows
import { wpGroupChat1 } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Team instantiated by GroupChat(agents=[...]) with a max_round and allowed speaker transitions.
 */
export const mastra = new Mastra({
  agents: {
    admin,
    planner,
    engineer,
    executor,
    writer,
    groupChatManager,
  },
  workflows: {
    wpGroupChat1,
  },
})
