/**
 * Workflow: email_agent_state_graph
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * WorkflowPattern generated from LangGraph StateGraph in index.ts
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { emailAssistantAgent } from '../agents'

// ── Workflow Steps ──

const taskWriteEmail = createStep({
  id: 'task_write_email',
  description: `You're an AI email assistant, tasked with writing an email for the user.`,
  inputSchema: z.object({CONVERSATION: z.string()}),
  outputSchema: z.object({subject: z.string(), to: z.string(), body: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You're an AI email assistant, tasked with writing an email for the user.
Use the entire conversation history between you, and the user to craft the email for them.

<conversation>
${context.CONVERSATION ?? ''}
</conversation>

If there is NOT enough information to send an email, respond to the user requesting the missing information.
Required fields:
- subject - The subject of the email
- body - The body of the email
- to - The recipient of the email`
    const result = await emailAssistantAgent.generate(prompt)
    return {
      ...context,
      subject: context.subject ?? result.text,
      to: context.to ?? result.text,
      body: context.body ?? result.text,
    }
  },
})

const taskInterrupt = createStep({
  id: 'task_interrupt',
  description: `# New Email`,
  inputSchema: z.object({subject: z.string(), to: z.string(), body: z.string()}),
  outputSchema: z.object({SUBJECT: z.string(), BODY: z.string(), TO: z.string(), USER_RESPONSE: z.string()}),
  execute: async ({ inputData }) => {
    // # New Email
    // TODO: Implement step logic
    throw new Error('task_interrupt not implemented yet')
  },
})

const taskRewriteEmail = createStep({
  id: 'task_rewrite_email',
  description: `You're an AI email assistant, tasked with rewriting an email for the user.`,
  inputSchema: z.object({SUBJECT: z.string(), BODY: z.string(), TO: z.string(), USER_RESPONSE: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You're an AI email assistant, tasked with rewriting an email for the user.
Here is the current state of the email for the user:
<email>
  <subject>
    ${context.SUBJECT ?? ''}
  </subject>
  <body>
    ${context.BODY ?? ''}
  </body>
  <to>
    ${context.TO ?? ''}
  </to>
</email>

Here is the user's response, which should contain some request for changes to the email:
<user-response>
${context.USER_RESPONSE ?? ''}
</user-response>

Given that, please rewrite the email. Do NOT modify anything the user does not request to be changed.`
    const result = await emailAssistantAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskSendEmail = createStep({
  id: 'task_send_email',
  description: `Render a confirmation UI indicating the email was successfully sent.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Render a confirmation UI indicating the email was successfully sent.`
    const result = await emailAssistantAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * email_agent_state_graph
 *
 * WorkflowPattern generated from LangGraph StateGraph in index.ts
 */
export const emailAgentStateGraph = createWorkflow({
  id: 'email_agent_state_graph',
  inputSchema: z.object({CONVERSATION: z.string()}),
  outputSchema: z.object({}),
  steps: [taskWriteEmail, taskInterrupt, taskRewriteEmail, taskSendEmail],
})
  .then(taskWriteEmail)
  .then(taskInterrupt)
  .then(taskRewriteEmail)
  .then(taskSendEmail)
  .commit()
