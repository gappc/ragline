<template>
  <MainLayout>
    <ChatSessionList class="hidden md:flex md:flex-col md:w-60" />
    <div class="flex flex-col flex-1 justify-between divide-y overflow-y-auto">
      <div
        ref="scrollWindow"
        class="flex flex-col items-center overflow-y-auto"
      >
        <ChatSession
          v-if="currentChatSession"
          :chat-session="currentChatSession"
          :loading="loading"
        />
      </div>
      <div class="py-6 flex justify-center">
        <InputPrompt
          :loading="loading"
          :abortController="abortController"
          @submit="submit"
        />
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";
import InputPrompt from "../components/input/InputPrompt.vue";
import MainLayout from "../layouts/MainLayout.vue";
import { useChatSessionStore } from "../modules/chatSession/chatSessionStore";
import ChatSession from "../modules/chatSession/components/ChatSession.vue";
import { useQuery } from "../modules/query/useQuery";
import ChatSessionList from "../modules/chatSession/components/ChatSessionList.vue";

const scrollWindow = ref<HTMLElement | null>(null);

const { loading, currentMessage, abortController, submitPrompt } = useQuery();

const { currentChatSessionId, currentChatSession, currentItems } = storeToRefs(
  useChatSessionStore()
);

const { loadChatSessions, initChatSession, addItem, updateItem } =
  useChatSessionStore();

// Load chat sessions
if (currentChatSessionId.value == null) {
  loadChatSessions();
}

watch(
  () => currentMessage.value,
  (answer) => {
    console.log(answer);

    if (answer != null) {
      const item = currentItems.value.at(-1);
      if (item != null) {
        item.answer = answer;
      }
    }
  }
);

watch(
  currentItems,
  () => {
    setTimeout(() => {
      scrollWindow.value?.scrollTo({
        top: scrollWindow.value.scrollHeight,
        behavior: "smooth",
      });
    }, 100);
  },
  {
    deep: true,
  }
);

const submit = async (prompt: string) => {
  const chatSessionId = currentChatSessionId.value ?? (await initChatSession());

  const index = addItem(chatSessionId, prompt);

  if (index == null) {
    console.error("Failed to add item");
    return;
  }

  const { promptId, answer, error, sources } = await submitPrompt(
    chatSessionId,
    prompt
  );

  updateItem(chatSessionId, index - 1, {
    promptId,
    prompt,
    answer,
    error,
    sources,
    feedback: null,
  });
};
</script>
