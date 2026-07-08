import { workflowRegistryServers } from "./src/mastra/workflows"

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env")
} catch {
  // no .env file present; rely on already-exported env vars instead
}

async function main() {
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowRegistryServers")
  console.log("=".repeat(80))

  const run1 = await workflowRegistryServers.createRunAsync()
  const result1 = await run1.start({
    inputData: {
      and_returning_raw_response_for_post: "",
    },
  })

  if (result1.status === "success") {
    console.log(result1.result)
  } else if (result1.status === "failed") {
    console.error(result1.error)
  } else {
    console.log(result1)
  }
}

main()
