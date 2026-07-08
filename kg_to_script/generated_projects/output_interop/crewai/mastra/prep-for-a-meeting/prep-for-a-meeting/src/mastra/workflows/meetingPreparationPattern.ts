/**
 * Workflow: meeting_preparation_pattern
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { researcherAgent, industryAnalystAgent, meetingStrategyAgent, summaryAndBriefingAgent } from '../agents'

// ── Workflow Steps ──

const researchTask = createStep({
  id: 'research_task',
  description: `Conduct comprehensive research on each of the individuals and companies`,
  inputSchema: z.object({participants: z.string(), context: z.string()}),
  outputSchema: z.object({participants: z.string(), context: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct comprehensive research on each of the individuals and companies
involved in the upcoming meeting. Gather information on recent
news, achievements, professional background, and any relevant
business activities.

Participants: ${context.participants ?? ''}
Meeting Context: ${context.context ?? ''}`
    const result = await researcherAgent.generate(prompt)
    return {
      ...context,
      participants: context.participants ?? result.text,
      context: context.context ?? result.text,
    }
  },
})

const industryAnalysisTask = createStep({
  id: 'industry_analysis_task',
  description: `Analyze the current industry trends, challenges, and opportunities`,
  inputSchema: z.object({participants: z.string(), context: z.string()}),
  outputSchema: z.object({context: z.string(), objective: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Analyze the current industry trends, challenges, and opportunities
relevant to the meeting's context. Consider market reports, recent
developments, and expert opinions to provide a comprehensive
overview of the industry landscape.

Participants: ${context.participants ?? ''}
Meeting Context: ${context.context ?? ''}`
    const result = await industryAnalystAgent.generate(prompt)
    return {
      ...context,
      context: context.context ?? result.text,
      objective: context.objective ?? result.text,
    }
  },
})

const meetingStrategyTask = createStep({
  id: 'meeting_strategy_task',
  description: `Develop strategic talking points, questions, and discussion angles`,
  inputSchema: z.object({context: z.string(), objective: z.string()}),
  outputSchema: z.object({context: z.string(), objective: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Develop strategic talking points, questions, and discussion angles
for the meeting based on the research and industry analysis conducted

Meeting Context: ${context.context ?? ''}
Meeting Objective: ${context.objective ?? ''}`
    const result = await meetingStrategyAgent.generate(prompt)
    return {
      ...context,
      context: context.context ?? result.text,
      objective: context.objective ?? result.text,
    }
  },
})

const summaryAndBriefingTask = createStep({
  id: 'summary_and_briefing_task',
  description: `Compile all the research findings, industry analysis, and strategic`,
  inputSchema: z.object({context: z.string(), objective: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Compile all the research findings, industry analysis, and strategic
talking points into a concise, comprehensive briefing document for
the meeting.
Ensure the briefing is easy to digest and equips the meeting
participants with all necessary information and strategies.

Meeting Context: ${context.context ?? ''}
Meeting Objective: ${context.objective ?? ''}`
    const result = await summaryAndBriefingAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * meeting_preparation_pattern
 */
export const meetingPreparationPattern = createWorkflow({
  id: 'meeting_preparation_pattern',
  inputSchema: z.object({participants: z.string(), context: z.string()}),
  outputSchema: z.object({}),
  steps: [researchTask, industryAnalysisTask, meetingStrategyTask, summaryAndBriefingTask],
})
  .then(researchTask)
  .then(industryAnalysisTask)
  .then(meetingStrategyTask)
  .then(summaryAndBriefingTask)
  .commit()
