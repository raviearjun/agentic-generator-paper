/**
 * Mastra AI Instance - MastraClientSystem
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Goal for the Mastra agent client: handle streaming responses, orchestrate client tool execution, and expose voice and observation endpoints.
 *   - : Provide stable streaming, tool execution continuation, and observability integration for agent runs.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { mastraAgentClient } from './agents'

// Import workflows
import { mastraAgentWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Represents the system/module that provides the Mastra agent client API implemented in agent1.ts.
 */
export const mastra = new Mastra({
  agents: {
    mastraAgentClient,
  },
  workflows: {
    mastraAgentWorkflow,
  },
})
