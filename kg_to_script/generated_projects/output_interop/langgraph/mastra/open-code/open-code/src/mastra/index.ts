/**
 * Mastra AI Instance - ProposedChangeUiTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Facilitate safe review and application of code changes via an agent-mediated user workflow.
 * Human Agents:
 *   - human_user ()
 */

import { Mastra } from '@mastra/core'

// Import agents
import { langgraphAgent } from './agents'

// Import workflows
import { workflowProposedChange } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Team representing the UI/system where a language agent presents proposed changes to a human and may call tools to apply accepted changes.
 */
export const mastra = new Mastra({
  agents: {
    langgraphAgent,
  },
  workflows: {
    workflowProposedChange,
  },
})
