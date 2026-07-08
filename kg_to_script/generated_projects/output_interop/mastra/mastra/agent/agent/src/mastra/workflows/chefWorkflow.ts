/**
 * Workflow: chef_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Sequential steps inferred from task functions in src/index.ts
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { chefAgent } from '../agents'

// ── Workflow Steps ──

const taskQueryPantry = createStep({
  id: 'task_query_pantry',
  description: `In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGenerateText = createStep({
  id: 'task_generate_text',
  description: `In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskTextStream = createStep({
  id: 'task_text_stream',
  description: `Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder.`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGenerateStream = createStep({
  id: 'task_generate_stream',
  description: `Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder.`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskTextObject = createStep({
  id: 'task_text_object',
  description: `I want to make lasagna, can you generate a lasagna recipe for me?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `I want to make lasagna, can you generate a lasagna recipe for me?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskTextObjectJsonschema = createStep({
  id: 'task_text_object_jsonschema',
  description: `I want to make lasagna, can you generate a lasagna recipe for me?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `I want to make lasagna, can you generate a lasagna recipe for me?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGenerateObject = createStep({
  id: 'task_generate_object',
  description: `I want to make lasagna, can you generate a lasagna recipe for me?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `I want to make lasagna, can you generate a lasagna recipe for me?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskStreamObject = createStep({
  id: 'task_stream_object',
  description: `I want to make lasagna, can you generate a lasagna recipe for me?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `I want to make lasagna, can you generate a lasagna recipe for me?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGenerateStreamObject = createStep({
  id: 'task_generate_stream_object',
  description: `I want to make lasagna, can you generate a lasagna recipe for me?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `I want to make lasagna, can you generate a lasagna recipe for me?`
    const result = await chefAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * chef_workflow
 *
 * Sequential steps inferred from task functions in src/index.ts
 */
export const chefWorkflow = createWorkflow({
  id: 'chef_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskQueryPantry, taskGenerateText, taskTextStream, taskGenerateStream, taskTextObject, taskTextObjectJsonschema, taskGenerateObject, taskStreamObject, taskGenerateStreamObject],
})
  .then(taskQueryPantry)
  .then(taskGenerateText)
  .then(taskTextStream)
  .then(taskGenerateStream)
  .then(taskTextObject)
  .then(taskTextObjectJsonschema)
  .then(taskGenerateObject)
  .then(taskStreamObject)
  .then(taskGenerateStreamObject)
  .commit()
