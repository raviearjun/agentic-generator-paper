/**
 * Workflow: mastra_agent_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * High-level workflow modeling the stream processing, client-tool execution, and continuation/recursion behavior implemented in agent1.ts.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { mastraAgentClient } from '../agents'

// ── Workflow Steps ──

const taskProcessRequest = createStep({
  id: 'task_process_request',
  description: `Process incoming generate/stream request: validate params, prepare requestContext and clientTools, and forward to server endpoints (/agents/{agentId}/generate or /agents/{agentId}/stream).`,
  inputSchema: z.object({agentId: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Process incoming generate/stream request: validate params, prepare requestContext and clientTools, and forward to server endpoints (/agents/${context.agentId ?? ''}/generate or /agents/${context.agentId ?? ''}/stream).`
    const result = await mastraAgentClient.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskExecuteClientTool = createStep({
  id: 'task_execute_client_tool',
  description: `Handle tool-call finish reason: locate pending client tool calls, execute \`clientTool.execute\`, attach observability data, synthesize tool-result chunks, and continue the stream/recursion as needed.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Handle tool-call finish reason: locate pending client tool calls, execute \`clientTool.execute\`, attach observability data, synthesize tool-result chunks, and continue the stream/recursion as needed.`
    const result = await mastraAgentClient.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskReturnResponse = createStep({
  id: 'task_return_response',
  description: `Finalize and return the response stream to the client; close controller when no client-tool continuation is required, or recursively continue the stream if client-tools were executed.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Finalize and return the response stream to the client; close controller when no client-tool continuation is required, or recursively continue the stream if client-tools were executed.`
    const result = await mastraAgentClient.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * mastra_agent_workflow
 *
 * High-level workflow modeling the stream processing, client-tool execution, and continuation/recursion behavior implemented in agent1.ts.
 */
export const mastraAgentWorkflow = createWorkflow({
  id: 'mastra_agent_workflow',
  inputSchema: z.object({agentId: z.string()}),
  outputSchema: z.object({}),
  steps: [taskProcessRequest, taskExecuteClientTool, taskReturnResponse],
})
  .then(taskProcessRequest)
  .then(taskExecuteClientTool)
  .then(taskReturnResponse)
  .commit()
