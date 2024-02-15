import { client } from "../api/client";
import { ChatEvent, ChatSession, FeedbackItem, Sentiment } from "./types";

interface ChatSessionDto {
  chat_session_id: string;
  name: string;
  created_at: string;
}

interface DocumentSourceDto {
  file: string;
  pages: number[];
}

interface FeedbackItemDto {
  text: string;
  date: string;
}

interface ChatResponseFeedback {
  sentiment: Sentiment;
  items: FeedbackItemDto[];
}

interface ChatEventDto {
  query_id: string | null;
  query: string;
  answer?: string | null;
  error?: string | null;
  sources?: DocumentSourceDto[];
  feedback?: ChatResponseFeedback | null;
}

export const fetchChatSessions = async (): Promise<ChatSession[]> => {
  const response = await client("/api/chat-sessions");
  const dtos: ChatSessionDto[] = await response.json();
  if (dtos.length === 0) {
    return [];
  }
  return dtos.map<ChatSession>((dto) => ({
    chatSessionId: dto.chat_session_id,
    name: dto.name,
    events: [],
    createdAt: new Date(dto.created_at),
  }));
};

export const fetchChatEvents = async (
  chatSessionId: string
): Promise<ChatEvent[]> => {
  const response = await client(`/api/chat-sessions/${chatSessionId}/events`);
  const dtos: ChatEventDto[] = await response.json();
  if (dtos.length === 0) {
    return [];
  }
  return dtos.map<ChatEvent>((dto) => ({
    promptId: dto.query_id,
    prompt: dto.query,
    answer: dto.answer ?? null,
    error: null,
    sources: [],
    feedback: {
      items:
        dto.feedback?.items.map<FeedbackItem>((item) => ({
          text: item.text,
          date: new Date(item.date),
        })) ?? [],
      sentiment: dto.feedback?.sentiment ?? "none",
    },
  }));
};
