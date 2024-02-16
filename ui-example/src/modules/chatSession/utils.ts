import { client } from "../api/client";
import { DocumentSource } from "../query/types";
import { ChatEvent, ChatSession, FeedbackItem, Sentiment } from "./types";

interface ChatSessionDto {
  chat_session_id: string;
  name: string;
  created_at: string;
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
  sources?: Record<string, number[]>;
  feedback?: ChatResponseFeedback | null;
}

export const fetchNewChatSession = async (): Promise<ChatSession> => {
  const response = await client("/api/chat-sessions", { method: "POST" });
  const dtos: ChatSessionDto = await response.json();
  return {
    chatSessionId: dtos.chat_session_id,
    name: dtos.name,
    events: [],
    createdAt: new Date(dtos.created_at),
  };
};

export const fetchDeleteChatSession = async (
  chatSessionId: string
): Promise<void> => {
  await client(`/api/chat-sessions/${chatSessionId}`, { method: "DELETE" });
};

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
    sources: computeSources(dto.sources),
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

export const computeSourcesBase64 = (
  sourcesBase64: string | null
): DocumentSource[] => {
  if (sourcesBase64 == null) {
    return [];
  }

  const sourcesString = atob(sourcesBase64);
  const sourcesObject: Record<string, number[]> = JSON.parse(sourcesString);

  return computeSources(sourcesObject);
};

export const computeSources = (
  sources: Record<string, number[]> | null | undefined
): DocumentSource[] => {
  if (sources == null) {
    return [];
  }
  return Object.entries(sources).map(([key, value]) => ({
    file: key,
    pages: value.sort((a, b) => a - b),
  }));
};
