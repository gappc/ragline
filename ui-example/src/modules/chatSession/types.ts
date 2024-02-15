import { DocumentSource } from "../query/types";

export type Sentiment = "none" | "good" | "bad";

export interface FeedbackItem {
  text: string;
  date: Date;
}

export interface ChatResponseFeedback {
  sentiment: Sentiment;
  items: FeedbackItem[];
}

export interface ChatEvent {
  prompt: string;
  promptId: string | null;
  answer: string | null;
  error: string | null;
  sources: DocumentSource[];
  feedback: ChatResponseFeedback | null;
}

export interface ChatSession {
  chatSessionId: string;
  name: string;
  events: ChatEvent[];
}
