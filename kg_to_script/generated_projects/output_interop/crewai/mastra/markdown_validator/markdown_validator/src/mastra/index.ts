/**
 * Mastra AI Instance - MarkDownValidatorCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Provide a detailed list of the markdown linting results.
Give a summary with actionable tasks to address the validation results.
Write your response as if you were handing it to a developer to fix the issues.
DO NOT provide examples of how to fix the issues or recommend other tools to use.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { requirementsManager } from './agents'

// Import workflows
import { markdownValidationWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    requirementsManager,
  },
  workflows: {
    markdownValidationWorkflow,
  },
})
