/**
 * Workflow: pattern_create_content
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { seniorContentEditor } from '../agents'

// ── Workflow Steps ──

const taskComponentContent = createStep({
  id: 'task_component_content',
  description: `A engineer will update the {component} (code below), return a list of good options of texts to replace EACH INDIVIDUAL existing text on the component, the suggestion MUST be based on the idea below, and also MUST be similar in length with the original text, we need to replace ALL TEXT.`,
  inputSchema: z.object({component: z.string(), expanded_idea: z.string(), file_content: z.string()}),
  outputSchema: z.object({component: z.string(), file_content: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `A engineer will update the ${context.component ?? ''} (code below), return a list of good options of texts to replace EACH INDIVIDUAL existing text on the component, the suggestion MUST be based on the idea below, and also MUST be similar in length with the original text, we need to replace ALL TEXT.

NEVER USE Apostrophes for contraction! You'll get a $100 tip if you do your best work!

IDEA
# -----
${context.expanded_idea ?? ''}

REACT COMPONENT CONTENT
# -----
${context.file_content ?? ''}`
    const result = await seniorContentEditor.generate(prompt)
    return {
      ...context,
      component: context.component ?? result.text,
      file_content: context.file_content ?? result.text,
    }
  },
})

const taskUpdateComponent = createStep({
  id: 'task_update_component',
  description: `YOU MUST USE the tool to write an updated version of the react component to the file system in the following path: {component} replacing the text content with the suggestions provided.`,
  inputSchema: z.object({component: z.string(), file_content: z.string()}),
  outputSchema: z.object({component: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `YOU MUST USE the tool to write an updated version of the react component to the file system in the following path: ${context.component ?? ''} replacing the text content with the suggestions provided.

You only modify the text content, you don't add or remove any components.

RULES
# -----
- Remove all the links, this should be single page landing page.
- Don't make up images, videos, gifs, icons, logos, etc.
- keep the same style and tailwind classes.
- MUST HAVE 'use client' at the be beginning of the code.
- href in buttons, links, NavLinks, and navigations should be \`#\`.
- NEVER WRITE \\n (newlines as string) on the file, just the code.
- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.
- Keep the same component imports and don't use new components.
- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.
- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.
- Save the file as with \`.jsx\` extension.

If you follow the rules I'll give you a $100 tip!!! MY LIFE DEPEND ON YOU FOLLOWING IT!

CONTENT TO BE UPDATED
# -----
${context.file_content ?? ''}`
    const result = await seniorContentEditor.generate(prompt)
    return {
      ...context,
      component: context.component ?? result.text,
    }
  },
})

const taskQaComponent = createStep({
  id: 'task_qa_component',
  description: `Check the React component code to make sure it's valid and abide by the rules below, if it doesn't then write the correct version to the file system using the write file tool into the following path: {component}.`,
  inputSchema: z.object({component: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Check the React component code to make sure it's valid and abide by the rules below, if it doesn't then write the correct version to the file system using the write file tool into the following path: ${context.component ?? ''}.

Your final answer should be a confirmation that the component is valid and abides by the rules and if you had to write an updated version to the file system.

RULES
# -----
- NEVER USE Apostrophes for contraction!
- ALL COMPONENTS USED SHOULD BE IMPORTED.
- MUST HAVE 'use client' at the be beginning of the code.
- href in buttons, links, NavLinks, and navigations should be \`#\`.
- NEVER WRITE \\n (newlines as string) on the file, just the code.
- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.
- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.
- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.
- Always use \`export function\` for the component class.

You'll get a $100 tip if you follow all the rules!`
    const result = await seniorContentEditor.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * pattern_create_content
 */
export const patternCreateContent = createWorkflow({
  id: 'pattern_create_content',
  inputSchema: z.object({component: z.string(), expanded_idea: z.string(), file_content: z.string()}),
  outputSchema: z.object({}),
  steps: [taskComponentContent, taskUpdateComponent, taskQaComponent],
})
  .then(taskComponentContent)
  .then(taskUpdateComponent)
  .then(taskQaComponent)
  .commit()
