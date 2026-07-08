/**
 * Workflow: buy_stock_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * A simple three-step flow: open UI, execute purchase, confirm purchase.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { tradeAgent } from '../agents'

// ── Workflow Steps ──

const openBuyUiTask = createStep({
  id: 'open_buy_ui_task',
  description: `Open the buy stock user interface for the specified ticker and prefill price information. Expected output: UI displayed and ready for user input.`,
  inputSchema: z.object({Expected_output: z.string()}),
  outputSchema: z.object({buy: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Open the buy stock user interface for the specified ticker and prefill price information. Expected output: UI displayed and ready for user input.`
    const result = await tradeAgent.generate(prompt)
    return {
      ...context,
      buy: context.buy ?? result.text,
    }
  },
})

const executePurchaseTask = createStep({
  id: 'execute_purchase_task',
  description: `Invoke the 'buy-stock' tool with JSON: { purchaseDetails: { ticker: <string>, quantity: <integer>, price: <number> } }. Expect the tool to return a confirmation payload.`,
  inputSchema: z.object({buy: z.string()}),
  outputSchema: z.object({Expected_output: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Invoke the 'buy-stock' tool with JSON: { purchaseDetails: { ticker: <string>, quantity: <integer>, price: <number> } }. Expect the tool to return a confirmation payload.`
    const result = await tradeAgent.generate(prompt)
    return {
      ...context,
      Expected_output: context.Expected_output ?? result.text,
    }
  },
})

const confirmPurchaseTask = createStep({
  id: 'confirm_purchase_task',
  description: `Present the purchase confirmation message to the user, showing ticker, quantity, price, and total cost. Expected output: confirmation message shown in UI.`,
  inputSchema: z.object({Expected_output: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Present the purchase confirmation message to the user, showing ticker, quantity, price, and total cost. Expected output: confirmation message shown in UI.`
    const result = await tradeAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * buy_stock_workflow
 *
 * A simple three-step flow: open UI, execute purchase, confirm purchase.
 */
export const buyStockWorkflow = createWorkflow({
  id: 'buy_stock_workflow',
  inputSchema: z.object({Expected_output: z.string()}),
  outputSchema: z.object({}),
  steps: [openBuyUiTask, executePurchaseTask, confirmPurchaseTask],
})
  .then(openBuyUiTask)
  .then(executePurchaseTask)
  .then(confirmPurchaseTask)
  .commit()
