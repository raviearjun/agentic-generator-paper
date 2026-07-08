/**
 * Workflow: onboarding_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { onboardingPersonalInformationAgent, onboardingTopicPreferenceAgent, customerEngagementAgent } from '../agents'

// ── Workflow Steps ──

const taskOnboardingPersonalInfo = createStep({
  id: 'task_onboarding_personal_info',
  description: `Hello, I'm here to help you get started with our product. Could you tell me your name and location?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Hello, I'm here to help you get started with our product. Could you tell me your name and location?`
    const result = await onboardingPersonalInformationAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskOnboardingTopicPreference = createStep({
  id: 'task_onboarding_topic_preference',
  description: `Great! Could you tell me what topics you are interested in reading about?`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Great! Could you tell me what topics you are interested in reading about?`
    const result = await onboardingTopicPreferenceAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskCustomerEngagementRequest = createStep({
  id: 'task_customer_engagement_request',
  description: `Let's find something fun to read.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Let's find something fun to read.`
    const result = await customerEngagementAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * onboarding_workflow
 */
export const onboardingWorkflow = createWorkflow({
  id: 'onboarding_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskOnboardingPersonalInfo, taskOnboardingTopicPreference, taskCustomerEngagementRequest],
})
  .then(taskOnboardingPersonalInfo)
  .then(taskOnboardingTopicPreference)
  .then(taskCustomerEngagementRequest)
  .commit()
