import { DocumentSource } from "../query/types";

export type Sentiment = "none" | "good" | "bad";

export interface FeedbackItem {
  text: string;
  date: Date;
}

export interface ConversationItemFeedback {
  sentiment: Sentiment;
  items: FeedbackItem[];
}

export interface ConversationItem {
  prompt: string;
  promptId: string | null;
  answer: string | null;
  error: string | null;
  sources: DocumentSource[];
  feedback: ConversationItemFeedback | null;
}

export interface ConversationContext {
  conversationId: string;
  conversationTitle: string;
  items: ConversationItem[];
}
