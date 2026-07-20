/**
 * Workflow: pattern_nested
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow pattern representing writer generation, critic initiation, sequential reviewers, and meta aggregation.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { unnamed, unnamed2, unnamed3, unnamed4, unnamed5, unnamed6 } from '../agents'

// ── Workflow Steps ──

const taskWriteBlog = createStep({
  id: 'task_write_blog',
  description: `撰写一篇简洁但引人入胜的博客，内容涉及`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `撰写一篇简洁但引人入胜的博客，内容涉及
       DeepLearning.AI. 确保博客100 字以内。

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed.generate(prompt)
    return { ...context, writeBlogOutput: result.text }
  },
})

const taskCriticInitiate1 = createStep({
  id: 'task_critic_initiate_1',
  description: `撰写一篇简洁但引人入胜的博客，内容涉及`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `撰写一篇简洁但引人入胜的博客，内容涉及
       DeepLearning.AI. 确保博客100 字以内。

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed2.generate(prompt)
    return { ...context, criticInitiate1Output: result.text }
  },
})

const taskNestedSeoReview = createStep({
  id: 'task_nested_seo_review',
  description: `仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}. 这里的 审查员 应该是你自己的角色`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}. 这里的 审查员 应该是你自己的角色

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed3.generate(prompt)
    return { ...context, seoReviewOutput: result.text }
  },
})

const taskNestedLegalReview = createStep({
  id: 'task_nested_legal_review',
  description: `仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed4.generate(prompt)
    return { ...context, legalReviewOutput: result.text }
  },
})

const taskNestedEthicsReview = createStep({
  id: 'task_nested_ethics_review',
  description: `仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed5.generate(prompt)
    return { ...context, ethicsReviewOutput: result.text }
  },
})

const taskMetaAggregate = createStep({
  id: 'task_meta_aggregate',
  description: `对所有审查员的反馈意见进行汇总，并对写作提出最终建议。`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `对所有审查员的反馈意见进行汇总，并对写作提出最终建议。

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed6.generate(prompt)
    return { ...context, metaAggregateOutput: result.text }
  },
})

const taskCriticInitiate2 = createStep({
  id: 'task_critic_initiate_2',
  description: `撰写一篇简洁但引人入胜的博客，内容涉及`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `撰写一篇简洁但引人入胜的博客，内容涉及
       DeepLearning.AI. 确保博客100 字以内。

Context from prior steps:
${JSON.stringify(context)}`
    const result = await unnamed2.generate(prompt)
    return { ...context, criticInitiate2Output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * pattern_nested
 *
 * Workflow pattern representing writer generation, critic initiation, sequential reviewers, and meta aggregation.
 */
export const patternNested = createWorkflow({
  id: 'pattern_nested',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskWriteBlog, taskCriticInitiate1, taskNestedSeoReview, taskNestedLegalReview, taskNestedEthicsReview, taskMetaAggregate, taskCriticInitiate2],
})
  .then(taskWriteBlog)
  .then(taskCriticInitiate1)
  .then(taskNestedSeoReview)
  .then(taskNestedLegalReview)
  .then(taskNestedEthicsReview)
  .then(taskMetaAggregate)
  .then(taskCriticInitiate2)
  .commit()
