/**
 * Workflow: stategraph_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { supervisor, router, stockbroker, tripPlanner, openCode, orderPizza, generalInput, writerAgent } from '../agents'

// ── Workflow Steps ──

const taskStart = createStep({
  id: 'task_start',
  description: `Start step for the supervisor StateGraph that initializes routing to the 'router' step.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Start step for the supervisor StateGraph that initializes routing to the 'router' step.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await supervisor.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskRouter = createStep({
  id: 'task_router',
  description: `The route to take based on the user's input.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `The route to take based on the user's input.
- stockbroker: can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio
- tripPlanner: helps the user plan their trip. it can suggest restaurants, and places to stay in any given location.
- openCode: can write a React TODO app for the user. Only call this tool if they request a TODO app.
- orderPizza: can order a pizza for the user
- writerAgent: can write a text document for the user. Only call this tool if they request a text document.
- generalInput: handles all other cases where the above tools don't apply

You're a highly helpful AI assistant, tasked with routing the user's query to the appropriate tool.
You should analyze the user's input, and choose the appropriate tool to use.

The expected output is a single route name: one of {stockbroker, tripPlanner, openCode, orderPizza, generalInput, writerAgent}.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await router.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskStockbroker = createStep({
  id: 'task_stockbroker',
  description: `Tool: stockbroker — can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Tool: stockbroker — can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await stockbroker.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskTripPlanner = createStep({
  id: 'task_trip_planner',
  description: `Tool: tripPlanner — helps the user plan their trip; can suggest restaurants and places to stay for a given location.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Tool: tripPlanner — helps the user plan their trip; can suggest restaurants and places to stay for a given location.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await tripPlanner.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskOpenCode = createStep({
  id: 'task_open_code',
  description: `Tool: openCode — can write a React TODO app for the user. Only call this tool if they request a TODO app.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Tool: openCode — can write a React TODO app for the user. Only call this tool if they request a TODO app.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await openCode.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskOrderPizza = createStep({
  id: 'task_order_pizza',
  description: `Tool: orderPizza — can order a pizza for the user.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Tool: orderPizza — can order a pizza for the user.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await orderPizza.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGeneralInput = createStep({
  id: 'task_general_input',
  description: `You are an AI assistant.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are an AI assistant.
If the user asks what you can do, describe these tools.
- stockbroker: can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio
- tripPlanner: helps the user plan their trip. it can suggest restaurants, and places to stay in any given location.
- openCode: can write a React TODO app for the user. Only call this tool if they request a TODO app.
- orderPizza: can order a pizza for the user
- writerAgent: can write a text document for the user. Only call this tool if they request a text document.

If the last message is a tool result, describe what the action was, congratulate the user, or send a friendly followup in response to the tool action. Ensure this is a clear and concise message.

Otherwise, just answer as normal.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await generalInput.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskWriterAgent = createStep({
  id: 'task_writer_agent',
  description: `Tool: writerAgent — can write a text document for the user. Only call this tool if they request a text document.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Tool: writerAgent — can write a text document for the user. Only call this tool if they request a text document.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await writerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskEnd = createStep({
  id: 'task_end',
  description: `End step for the supervisor StateGraph indicating the workflow is complete.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `End step for the supervisor StateGraph indicating the workflow is complete.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await supervisor.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * stategraph_workflow
 */
export const stategraphWorkflow = createWorkflow({
  id: 'stategraph_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskStart, taskRouter, taskStockbroker, taskTripPlanner, taskOpenCode, taskOrderPizza, taskGeneralInput, taskWriterAgent, taskEnd],
})
  // NOTE: Branching workflow — simplified to sequential for type compatibility
  // TODO: Implement conditional branching using .branch() API
  .then(taskStart)
  .then(taskRouter)
  .then(taskStockbroker)
  .then(taskTripPlanner)
  .then(taskOpenCode)
  .then(taskOrderPizza)
  .then(taskGeneralInput)
  .then(taskWriterAgent)
  .then(taskEnd)
  .commit()
