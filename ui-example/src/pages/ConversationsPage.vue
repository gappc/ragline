<template>
  <MainLayout>
    <div class="flex flex-col flex-1 justify-between divide-y overflow-y-auto">
      <div
        ref="scrollWindow"
        class="flex flex-col items-center overflow-y-auto"
      >
        <Conversation
          v-if="currentConversation"
          :conversation="currentConversation"
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
import { ref, watch } from "vue";
import MainLayout from "../layouts/MainLayout.vue";
import Conversation from "../modules/conversation/components/Conversation.vue";
import { useConversationStore } from "../modules/conversation/conversationStore";
import { useQuery } from "../modules/query/useQuery";
import InputPrompt from "../components/input/InputPrompt.vue";
import { storeToRefs } from "pinia";

const scrollWindow = ref<HTMLElement | null>(null);

const { loading, currentMessage, abortController, submitPrompt } = useQuery();

const { currentConversationId, currentConversation, currentItems } =
  storeToRefs(useConversationStore());

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
  if (currentConversationId.value == null) {
    return;
  }

  const { addItem, updateItem } = useConversationStore();

  const index = addItem(currentConversationId.value, prompt);

  if (index == null) {
    return;
  }

  const { promptId, answer, error, sources } = await submitPrompt(
    currentConversationId.value,
    prompt
  );

  updateItem(currentConversationId.value, index - 1, {
    promptId,
    prompt,
    answer,
    error,
    sources,
    feedback: null,
  });
};
</script>
