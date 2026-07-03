/**
 * Mastra AI Instance - GenerativeUiAgent
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 */

import { Mastra } from '@mastra/core'

// Import agents
import { supervisor, router, generalInput, stockbroker, tripPlanner, openCode, orderPizza, writerAgent } from './agents'

// Import workflows
import { stategraphWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    supervisor,
    router,
    generalInput,
    stockbroker,
    tripPlanner,
    openCode,
    orderPizza,
    writerAgent,
  },
  workflows: {
    stategraphWorkflow,
  },
})
