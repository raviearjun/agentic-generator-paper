import { wpOpenApiSpecGenWorkflow, wpMakePrToMastra } from "./src/mastra/workflows"

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env")
} catch {
  // no .env file present; rely on already-exported env vars instead
}

async function main() {
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: wpOpenApiSpecGenWorkflow")
  console.log("=".repeat(80))

  const run1 = await wpOpenApiSpecGenWorkflow.createRunAsync()
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
  console.log("Workflow: wpMakePrToMastra")
  console.log("=".repeat(80))

  const run2 = await wpMakePrToMastra.createRunAsync()
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
}

main()
