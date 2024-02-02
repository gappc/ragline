import { acceptHMRUpdate, defineStore } from "pinia";
import { ConversationContext, ConversationItem } from "./types";

interface State {
  currentConversationId: string | null;
  conversations: ConversationContext[];
}

const initialState: State = {
  currentConversationId: "1",
  conversations: [
    {
      conversationId: "1",
      conversationTitle: "Chat 1",
      items: [
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

export const useConversationStore = defineStore("conversationStore", {
  state: () => initialState,
  getters: {
    currentConversation(state): ConversationContext | undefined {
      return state.conversations.find(
        (c) => c.conversationId === state.currentConversationId
      );
    },
    currentItems(): ConversationItem[] {
      return this.currentConversation != null
        ? this.currentConversation.items
        : [];
    },
  },
  actions: {
    setCurrentConversation(conversationId: string) {
      this.currentConversationId = conversationId;
    },
    addItem(conversationId: string, itemOrPrompt: ConversationItem | string) {
      const conversation = this.conversations.find(
        (c) => c.conversationId === conversationId
      );
      if (!conversation) {
        return;
      }
      const item: ConversationItem =
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

      return conversation.items.push(item);
    },
    updateItem(conversationId: string, index: number, item: ConversationItem) {
      const conversation = this.conversations.find(
        (c) => c.conversationId === conversationId
      );
      if (
        conversation == null ||
        index < 0 ||
        index >= conversation.items.length
      ) {
        return;
      }
      conversation.items[index] = item;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useConversationStore, import.meta.hot)
  );
}
