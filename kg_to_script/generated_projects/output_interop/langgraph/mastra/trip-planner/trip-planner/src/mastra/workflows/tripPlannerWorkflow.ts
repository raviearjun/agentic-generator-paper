/**
 * Workflow: trip_planner_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Inferred workflow representing the user flow in the accommodations and restaurants UI: view list -> select item -> confirm/book -> show booked confirmation.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { tripPlannerAgent } from '../agents'

// ── Workflow Steps ──

const viewAccommodationsTask = createStep({
  id: 'view_accommodations_task',
  description: `List available accommodations with images, ratings, price, and brief details. Allow the user to open details of an accommodation.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `List available accommodations with images, ratings, price, and brief details. Allow the user to open details of an accommodation.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await tripPlannerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const selectAccommodationTask = createStep({
  id: 'select_accommodation_task',
  description: `When a user selects an accommodation, present full details (name, rating, price, dates, guests) and provide a booking action trigger.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `When a user selects an accommodation, present full details (name, rating, price, dates, guests) and provide a booking action trigger.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await tripPlannerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const confirmBookingTask = createStep({
  id: 'confirm_booking_task',
  description: `Construct a JSON payload with fields { accommodation, tripDetails } and call the 'book-accommodation' tool. After tool invocation, provide a human-facing confirmation message describing the booked accommodation and trip summary.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Construct a JSON payload with fields { accommodation, tripDetails } and call the 'book-accommodation' tool. After tool invocation, provide a human-facing confirmation message describing the booked accommodation and trip summary.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await tripPlannerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const bookedConfirmationTask = createStep({
  id: 'booked_confirmation_task',
  description: `Show booked accommodation summary including dates, guest count, address/name, rating and total price. If tool response includes booking reference, display it.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Show booked accommodation summary including dates, guest count, address/name, rating and total price. If tool response includes booking reference, display it.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await tripPlannerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * trip_planner_workflow
 *
 * Inferred workflow representing the user flow in the accommodations and restaurants UI: view list -> select item -> confirm/book -> show booked confirmation.
 */
export const tripPlannerWorkflow = createWorkflow({
  id: 'trip_planner_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [viewAccommodationsTask, selectAccommodationTask, confirmBookingTask, bookedConfirmationTask],
})
  .then(viewAccommodationsTask)
  .then(selectAccommodationTask)
  .then(confirmBookingTask)
  .then(bookedConfirmationTask)
  .commit()
