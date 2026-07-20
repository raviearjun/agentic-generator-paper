/**
 * Workflow: a2_a_client_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Representative sequence of A2A client interactions exposed by the A2A class.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { agentIdConstructorParameter } from '../agents'

// ── Workflow Steps ──

const taskGetAgentCard = createStep({
  id: 'task_get_agent_card',
  description: `Request agent card metadata via GET /.well-known/{agentId}/agent-card.json or via JSON-RPC agent/getAuthenticatedExtendedCard.`,
  inputSchema: z.object({agentId: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Request agent card metadata via GET /.well-known/${context.agentId ?? ''}/agent-card.json or via JSON-RPC agent/getAuthenticatedExtendedCard.`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskSendMessage = createStep({
  id: 'task_send_message',
  description: `Send a message to the agent using JSON-RPC method message/send with MessageSendParams.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Send a message to the agent using JSON-RPC method message/send with MessageSendParams.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskSendMessageStream = createStep({
  id: 'task_send_message_stream',
  description: `Open a message/stream JSON-RPC request (SSE) to receive incremental A2A events for the initiated message/task.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Open a message/stream JSON-RPC request (SSE) to receive incremental A2A events for the initiated message/task.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGetTask = createStep({
  id: 'task_get_task',
  description: `Call tasks/get JSON-RPC with TaskQueryParams to retrieve task status and result.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/get JSON-RPC with TaskQueryParams to retrieve task status and result.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskCancelTask = createStep({
  id: 'task_cancel_task',
  description: `Call tasks/cancel JSON-RPC with TaskQueryParams to cancel a running task.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/cancel JSON-RPC with TaskQueryParams to cancel a running task.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskResubscribeTask = createStep({
  id: 'task_resubscribe_task',
  description: `Call tasks/resubscribe JSON-RPC with TaskIdParams and stream true to reattach to an existing task stream.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/resubscribe JSON-RPC with TaskIdParams and stream true to reattach to an existing task stream.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskSetPushNotificationConfig = createStep({
  id: 'task_set_push_notification_config',
  description: `Call tasks/pushNotificationConfig/set JSON-RPC with a TaskPushNotificationConfig object.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/pushNotificationConfig/set JSON-RPC with a TaskPushNotificationConfig object.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGetPushNotificationConfig = createStep({
  id: 'task_get_push_notification_config',
  description: `Call tasks/pushNotificationConfig/get JSON-RPC with identifying params.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/pushNotificationConfig/get JSON-RPC with identifying params.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskListPushNotificationConfig = createStep({
  id: 'task_list_push_notification_config',
  description: `Call tasks/pushNotificationConfig/list JSON-RPC to retrieve configurations.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/pushNotificationConfig/list JSON-RPC to retrieve configurations.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskDeletePushNotificationConfig = createStep({
  id: 'task_delete_push_notification_config',
  description: `Call tasks/pushNotificationConfig/delete JSON-RPC with identifying params to delete a config.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call tasks/pushNotificationConfig/delete JSON-RPC with identifying params to delete a config.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await agentIdConstructorParameter.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * a2_a_client_workflow
 *
 * Representative sequence of A2A client interactions exposed by the A2A class.
 */
export const a2AClientWorkflow = createWorkflow({
  id: 'a2_a_client_workflow',
  inputSchema: z.object({agentId: z.string()}),
  outputSchema: z.object({}),
  steps: [taskGetAgentCard, taskSendMessage, taskSendMessageStream, taskGetTask, taskCancelTask, taskResubscribeTask, taskSetPushNotificationConfig, taskGetPushNotificationConfig, taskListPushNotificationConfig, taskDeletePushNotificationConfig],
})
  .then(taskGetAgentCard)
  .then(taskSendMessage)
  .then(taskSendMessageStream)
  .then(taskGetTask)
  .then(taskCancelTask)
  .then(taskResubscribeTask)
  .then(taskSetPushNotificationConfig)
  .then(taskGetPushNotificationConfig)
  .then(taskListPushNotificationConfig)
  .then(taskDeletePushNotificationConfig)
  .commit()
