/**
 * Mastra AI Instance - Teamexpandidea
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Understand and expand upon the essence of ideas, make sure they are great and focus on real pain points others could benefit from.
 *   - : Craft compelling stories using the Golden Circle method to captivate and engage people around an idea.
 *   - : Build an intuitive, aesthetically pleasing, and high-converting landing page.
 *   - : Ensure the landing page content is clear, concise, and captivating.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { seniorIdeaAnalyst, seniorStrategist, seniorReactEngineer, seniorContentEditor } from './agents'

// Import workflows
import { patternExpandIdea, patternChooseTemplate, patternCreateContent } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    seniorIdeaAnalyst,
    seniorStrategist,
    seniorReactEngineer,
    seniorContentEditor,
  },
  workflows: {
    patternExpandIdea,
    patternChooseTemplate,
    patternCreateContent,
  },
})
