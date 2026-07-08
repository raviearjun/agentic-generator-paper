/**
 * Agent: Planner
 * ID: Planner
 * 
 * Auto-generated from AgentO Knowledge Graph
 */

import { Agent } from '@mastra/core/agent'

/**
 * Planner
 * 
 * Instructions:
 * You are Planner.
 */
export const planner = new Agent({
  id: `Planner`,
  name: `Planner`,
  instructions: `You are Planner.`,
  model: 'openai/gpt-4o-mini',
})
