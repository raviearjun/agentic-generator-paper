import { patternExpandIdea, patternChooseTemplate, patternCreateContent } from "./src/mastra/workflows"

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env")
} catch {
  // no .env file present; rely on already-exported env vars instead
}

async function main() {
  console.log("\n" + "=".repeat(80))
  console.log("Workflow: patternExpandIdea")
  console.log("=".repeat(80))

  const run1 = await patternExpandIdea.createRunAsync()
  const result1 = await run1.start({
    inputData: {
      idea: "",
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
  console.log("Workflow: patternChooseTemplate")
  console.log("=".repeat(80))

  const run2 = await patternChooseTemplate.createRunAsync()
  const result2 = await run2.start({
    inputData: {
      idea: "",
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
  console.log("Workflow: patternCreateContent")
  console.log("=".repeat(80))

  const run3 = await patternCreateContent.createRunAsync()
  const result3 = await run3.start({
    inputData: {
      component: "",
      expanded_idea: "",
      file_content: "",
    },
  })

  if (result3.status === "success") {
    console.log(result3.result)
  } else if (result3.status === "failed") {
    console.error(result3.error)
  } else {
    console.log(result3)
  }
}

main()
