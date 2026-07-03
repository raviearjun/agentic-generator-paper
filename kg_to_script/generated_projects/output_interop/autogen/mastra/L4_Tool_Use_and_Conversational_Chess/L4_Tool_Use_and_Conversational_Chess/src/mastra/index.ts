/**
 * Mastra AI Instance - ConversationalChessTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Team-level goal: have the agents play a game of chess via conversational tool calls.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { playerWhite, playerBlack, boardProxy } from './agents'

// Import workflows
import { wpChessNested } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * A small team consisting of two player agents and a board proxy orchestrating the game.
 */
export const mastra = new Mastra({
  agents: {
    playerWhite,
    playerBlack,
    boardProxy,
  },
  workflows: {
    wpChessNested,
  },
})
