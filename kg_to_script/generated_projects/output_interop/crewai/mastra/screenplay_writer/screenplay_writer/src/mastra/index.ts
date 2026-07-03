/**
 * Mastra AI Instance - AiCrewforscreenwriting
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Create a screenplay from a newsgroup post.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { spamfilter, analyst, scriptwriter, formatter, scorer } from './agents'

// Import workflows
import { crewSequentialWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Crew.ai based crew that analyses a discussion, turns it into screenplay dialogue and formats it.
 */
export const mastra = new Mastra({
  agents: {
    spamfilter,
    analyst,
    scriptwriter,
    formatter,
    scorer,
  },
  workflows: {
    crewSequentialWorkflow,
  },
})
