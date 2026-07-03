/**
 * Agent: 逗哏 / stand-up comedian (performer)
 * ID: 郭德纲
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
 * 逗哏 / stand-up comedian (performer)
 * 
 * Instructions:
 * You are 逗哏 / stand-up comedian (performer).
 */
export const unnamed = new Agent({
  id: `郭德纲`,
  name: `逗哏 / stand-up comedian (performer)`,
  instructions: `You are 逗哏 / stand-up comedian (performer).`,
  model: 'openai/gpt-4o-mini',
  tools: {
    toolOpenAiApi,
  },
})
