/**
 * Agent: Writer
 * ID: Writer
 * 
 * Auto-generated from AgentO Knowledge Graph
 */

import { Agent } from '@mastra/core/agent'

/**
 * Writer
 * 
 * Instructions:
 * You are Writer.
 */
export const writer = new Agent({
  id: `Writer`,
  name: `Writer`,
  instructions: `You are Writer.`,
  model: 'openai/gpt-4o-mini',
})
