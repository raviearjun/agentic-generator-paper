/**
 * Agent: Engineer
 * ID: Engineer
 * 
 * Auto-generated from AgentO Knowledge Graph
 */

import { Agent } from '@mastra/core/agent'

/**
 * Engineer
 * 
 * Instructions:
 * You are Engineer.
 */
export const engineer = new Agent({
  id: `Engineer`,
  name: `Engineer`,
  instructions: `You are Engineer.`,
  model: 'openai/gpt-4o-mini',
})
