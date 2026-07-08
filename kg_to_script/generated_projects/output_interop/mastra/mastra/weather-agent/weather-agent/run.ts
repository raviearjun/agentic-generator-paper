import { workflowWeatherWorkflow } from "./src/mastra/workflows"

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env")
} catch {
  // no .env file present; rely on already-exported env vars instead
}

async function main() {
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowWeatherWorkflow")
  console.log("=".repeat(80))

  const run1 = await workflowWeatherWorkflow.createRunAsync()
  const result1 = await run1.start({
    inputData: {
      city_as_input_to_retrieve_forecast_data_from_the_Open: "",
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
