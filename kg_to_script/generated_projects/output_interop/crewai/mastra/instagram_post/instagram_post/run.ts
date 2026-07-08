import { workflowCopyCrew, workflowImageCrew } from "./src/mastra/workflows"

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env")
} catch {
  // no .env file present; rely on already-exported env vars instead
}

async function main() {
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: workflowCopyCrew")
  console.log("=".repeat(80))

  const run1 = await workflowCopyCrew.createRun()
  const result1 = await run1.start({
    inputData: {
      product_website: "",
      product_details: "",
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
  console.log("Workflow: workflowImageCrew")
  console.log("=".repeat(80))

  const run2 = await workflowImageCrew.createRun()
  const result2 = await run2.start({
    inputData: {
      copy: "",
      product_website: "",
      product_details: "",
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
