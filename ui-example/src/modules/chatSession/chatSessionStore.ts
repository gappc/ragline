import { acceptHMRUpdate, defineStore } from "pinia";
import { ChatSession, ChatEvent } from "./types";

interface State {
  currentChatSessionId: string | null;
  chatSessions: ChatSession[];
}

const initialState: State = {
  currentChatSessionId: "34c77cc87e634be28a9f482d4a68d5bd",
  chatSessions: [
    {
      chatSessionId: "34c77cc87e634be28a9f482d4a68d5bd",
      name: "Chat 1",
      events: [
        {
          promptId: "1",
          prompt: "What is the meaning of life?",
          answer: "42",
          error: null,
          sources: [],
          feedback: null,
        },
        {
          promptId: "2",
          prompt: "How many roads?",
          answer: "12",
          error: null,
          sources: [
            {
              file: "file1",
              pages: [1, 2, 3],
            },
            {
              file: "file2",
              pages: [4, 5, 6],
            },
          ],
          feedback: {
            sentiment: "bad",
            items: [],
          },
        },
        {
          promptId: "3",
          prompt: "Why is the sky blue?",
          answer: "Because it is",
          error: null,
          sources: [],
          feedback: {
            sentiment: "good",
            items: [
              {
                text: "I like this answer",
                date: new Date(),
              },
              {
                text: "Yes, really nice",
                date: new Date(),
              },
            ],
          },
        },
      ],
    },
  ],
};

export const useChatSessionStore = defineStore("chatSessionStore", {
  state: () => initialState,
  getters: {
    currentChatSession(state): ChatSession | undefined {
      return state.chatSessions.find(
        (c) => c.chatSessionId === state.currentChatSessionId
      );
    },
    currentItems(): ChatEvent[] {
      return this.currentChatSession != null
        ? this.currentChatSession.events
        : [];
    },
  },
  actions: {
    setCurrentChatSession(chatSessionId: string) {
      this.currentChatSessionId = chatSessionId;
    },
    addItem(chatSessionId: string, itemOrPrompt: ChatEvent | string) {
      const chatSession = this.chatSessions.find(
        (c) => c.chatSessionId === chatSessionId
      );
      if (!chatSession) {
        return;
      }
      const item: ChatEvent =
        typeof itemOrPrompt === "string"
          ? {
              promptId: null,
              prompt: itemOrPrompt,
              answer: null,
              error: null,
              sources: [],
              feedback: null,
            }
          : itemOrPrompt;

      return chatSession.events.push(item);
    },
    updateItem(chatSessionId: string, index: number, item: ChatEvent) {
      const chatSession = this.chatSessions.find(
        (c) => c.chatSessionId === chatSessionId
      );
      if (
        chatSession == null ||
        index < 0 ||
        index >= chatSession.events.length
      ) {
        return;
      }
      chatSession.events[index] = item;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useChatSessionStore, import.meta.hot));
}
