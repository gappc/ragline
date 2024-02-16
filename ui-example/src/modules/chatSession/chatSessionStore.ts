import { acceptHMRUpdate, defineStore } from "pinia";
import { ChatEvent, ChatSession } from "./types";
import {
  fetchChatEvents,
  fetchChatSessions,
  fetchDeleteChatSession,
  fetchNewChatSession,
} from "./utils";

interface State {
  currentChatSessionId: string | null;
  chatSessions: ChatSession[];
}

const initialState: State = {
  currentChatSessionId: null,
  chatSessions: [],
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
    async loadChatSessions() {
      this.chatSessions = await fetchChatSessions();
      if (this.chatSessions.length > 0) {
        await this.setCurrentChatSession(this.chatSessions[0].chatSessionId);
      }
    },
    async initChatSession() {
      const chatSession = await fetchNewChatSession();
      this.currentChatSessionId = chatSession.chatSessionId;
      this.chatSessions = [chatSession, ...this.chatSessions];

      return this.currentChatSessionId;
    },
    async setCurrentChatSession(chatSessionId: string | null) {
      this.currentChatSessionId = chatSessionId;

      if (chatSessionId != null) {
        const chatEvents = await fetchChatEvents(chatSessionId);

        this.currentChatSessionId = chatSessionId;

        if (this.currentChatSession != null) {
          this.currentChatSession.events = chatEvents;
        }
      }
    },
    async deleteChatSession(chatSessionId: string) {
      await fetchDeleteChatSession(chatSessionId);
      this.chatSessions = this.chatSessions.filter(
        (c) => c.chatSessionId !== chatSessionId
      );
      this.setCurrentChatSession(null);
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
    reset() {
      this.$reset();
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useChatSessionStore, import.meta.hot));
}
