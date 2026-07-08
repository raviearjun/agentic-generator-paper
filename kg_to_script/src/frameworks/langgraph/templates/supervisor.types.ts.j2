import { Annotation } from "@langchain/langgraph";

export const SupervisorAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each routed node only returns its own
    // new message(s), so the reducer must accumulate history or every
    // subsequent route only ever sees the immediately preceding node's
    // output instead of the full conversation.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
  next: Annotation<string>({
    // `next` is a one-shot routing decision, not accumulated history —
    // replacing it each time is correct here, unlike `messages` above.
    reducer: (_, next) => next,
    default: () => "",
  }),
});

export type SupervisorState = typeof SupervisorAnnotation.State;
export type SupervisorUpdate = typeof SupervisorAnnotation.Update;
