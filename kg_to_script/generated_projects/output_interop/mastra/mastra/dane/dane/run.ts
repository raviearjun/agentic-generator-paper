import { workflowChangelog, workflowEntry, workflowCommitMessage, workflowGithubFirstContributorMessage, workflowGithubIssueLabeler, workflowLinkChecker, workflowPnpmChangsetPublisher, workflowTelephoneGame } from "./src/mastra/workflows"

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env")
} catch {
  // no .env file present; rely on already-exported env vars instead
}

async function main() {
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowChangelog")
  console.log("=".repeat(80))

  const run1 = await workflowChangelog.createRunAsync()
  const result1 = await run1.start({
    inputData: {
      input: "",
    },
  })

  if (result1.status === "success") {
    console.log(result1.result)
  } else if (result1.status === "failed") {
    console.error(result1.error)
  } else {
    console.log(result1)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowEntry")
  console.log("=".repeat(80))

  const run2 = await workflowEntry.createRunAsync()
  const result2 = await run2.start({
    inputData: {
      input: "",
    },
  })

  if (result2.status === "success") {
    console.log(result2.result)
  } else if (result2.status === "failed") {
    console.error(result2.error)
  } else {
    console.log(result2)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowCommitMessage")
  console.log("=".repeat(80))

  const run3 = await workflowCommitMessage.createRunAsync()
  const result3 = await run3.start({
    inputData: {
      input: "",
    },
  })

  if (result3.status === "success") {
    console.log(result3.result)
  } else if (result3.status === "failed") {
    console.error(result3.error)
  } else {
    console.log(result3)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowGithubFirstContributorMessage")
  console.log("=".repeat(80))

  const run4 = await workflowGithubFirstContributorMessage.createRunAsync()
  const result4 = await run4.start({
    inputData: {
      input: "",
    },
  })

  if (result4.status === "success") {
    console.log(result4.result)
  } else if (result4.status === "failed") {
    console.error(result4.error)
  } else {
    console.log(result4)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowGithubIssueLabeler")
  console.log("=".repeat(80))

  const run5 = await workflowGithubIssueLabeler.createRunAsync()
  const result5 = await run5.start({
    inputData: {
      input: "",
    },
  })

  if (result5.status === "success") {
    console.log(result5.result)
  } else if (result5.status === "failed") {
    console.error(result5.error)
  } else {
    console.log(result5)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowLinkChecker")
  console.log("=".repeat(80))

  const run6 = await workflowLinkChecker.createRunAsync()
  const result6 = await run6.start({
    inputData: {
      input: "",
    },
  })

  if (result6.status === "success") {
    console.log(result6.result)
  } else if (result6.status === "failed") {
    console.error(result6.error)
  } else {
    console.log(result6)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowPnpmChangsetPublisher")
  console.log("=".repeat(80))

  const run7 = await workflowPnpmChangsetPublisher.createRunAsync()
  const result7 = await run7.start({
    inputData: {
      CRITICAL: "",
      Include_create: "",
    },
  })

  if (result7.status === "success") {
    console.log(result7.result)
  } else if (result7.status === "failed") {
    console.error(result7.error)
  } else {
    console.log(result7)
  }
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowTelephoneGame")
  console.log("=".repeat(80))

  const run8 = await workflowTelephoneGame.createRunAsync()
  const result8 = await run8.start({
    inputData: {
      input: "",
    },
  })

  if (result8.status === "success") {
    console.log(result8.result)
  } else if (result8.status === "failed") {
    console.error(result8.error)
  } else {
    console.log(result8)
  }
}

main()
