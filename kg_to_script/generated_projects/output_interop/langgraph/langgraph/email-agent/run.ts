import { graph } from "./index.js";

// Node 20.6+ built-in .env loader - avoids needing the `dotenv` package,
// which isn't in this project's package.json.
try {
  process.loadEnvFile(".env");
} catch {
  // no .env file present; rely on already-exported env vars instead
}

// Fill in real values for each field below, then run with `npm run dev`.
const inputs: Record<string, string> = {
  CONVERSATION: "Write an email to Alex (alex@example.com) letting them know the product launch has been moved from June 10 to June 24, and ask them to update the marketing calendar accordingly.",
  subject: "",
  to: "",
  body: "",
  SUBJECT: "",
  BODY: "",
  TO: "",
  USER_RESPONSE: "Can you make the tone more casual and mention it's now a two-week delay?",
};

async function main() {
  const seed = {
    messages: [
      {
        role: "user",
        content: Object.entries(inputs)
          .map(([key, value]) => `${key}: ${value}`)
          .join("\n"),
      },
    ],
  };

  for await (const chunk of await graph.stream(seed, { streamMode: "updates" })) {
    for (const [nodeName, update] of Object.entries(chunk)) {
      console.log("\n" + "=".repeat(80));
      console.log(`Node: ${nodeName}`);
      console.log("=".repeat(80));
      const messages = (update as { messages?: { content?: string }[] })?.messages;
      const last = messages?.[messages.length - 1];
      console.log(last?.content ?? update);
    }
  }
}

main();
