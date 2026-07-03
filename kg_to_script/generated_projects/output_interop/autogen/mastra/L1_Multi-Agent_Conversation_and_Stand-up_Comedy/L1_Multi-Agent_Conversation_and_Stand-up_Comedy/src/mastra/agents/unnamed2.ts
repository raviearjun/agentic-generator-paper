/**
 * Agent: 捧哏 / stand-up partner (support)
 * ID: 于谦
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Capabilities:
 *   - : Provides LLM inference and chat functionality.
 *   - : Retrieves OpenAI API key from environment or secret store.
 */

import { Agent } from '@mastra/core/agent'

// Import tools
import { toolOpenAiApi } from '../tools'

/**
 * 捧哏 / stand-up partner (support)
 * 
 * Instructions:
 * You are 捧哏 / stand-up partner (support).
 */
export const unnamed2 = new Agent({
  id: `于谦`,
  name: `捧哏 / stand-up partner (support)`,
  instructions: `You are 捧哏 / stand-up partner (support).`,
  model: 'openai/gpt-4o-mini',
  tools: {
    toolOpenAiApi,
  },
})
