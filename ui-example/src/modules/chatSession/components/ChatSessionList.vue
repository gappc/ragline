<template>
  <div>
    <ButtonCustom
      size="sm"
      class="mt-2 mb-4 mr-2"
      @click="setCurrentChatSession(null)"
    >
      New Chat
    </ButtonCustom>
    <div class="flex flex-col gap-3 overflow-y-auto pr-2">
      <div
        v-for="chatSession in chatSessions"
        :key="chatSession.chatSessionId"
        class="flex justify-between items-center"
      >
        <button
          class="text-left"
          :class="{
            'font-bold': chatSession.chatSessionId === currentChatSessionId,
          }"
          @click="setCurrentChatSession(chatSession.chatSessionId)"
        >
          {{ useDateFormat(chatSession.createdAt, "YYYY-MM-DD HH:mm:ss") }}
        </button>
        <ButtonCustom
          size="xs"
          variant="ghost"
          class="p-2"
          @click="statefulDeleteChatSession(chatSession.chatSessionId)"
        >
          <IconDelete
            v-if="deletingChatSessionId !== chatSession.chatSessionId"
            class="w-4 h-4 fill-red-500"
          />
          <IconThumbUp v-else class="w-4 h-4 fill-red-500" />
        </ButtonCustom>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useChatSessionStore } from "../chatSessionStore";
import { useDateFormat } from "@vueuse/core";
import ButtonCustom from "../../../components/button/ButtonCustom.vue";
import IconDelete from "../../../components/svg/IconDelete.vue";
import { ref } from "vue";
import IconThumbUp from "../../../components/svg/IconThumbUp.vue";

const deletingChatSessionId = ref<string | null>(null);

const { chatSessions, currentChatSessionId } = storeToRefs(
  useChatSessionStore()
);

const { setCurrentChatSession, deleteChatSession } = useChatSessionStore();

const statefulDeleteChatSession = async (chatSessionId: string) => {
  if (deletingChatSessionId.value !== chatSessionId) {
    deletingChatSessionId.value = chatSessionId;
    setTimeout(() => {
      deletingChatSessionId.value = null;
    }, 3000);
    return;
  }
  if (deletingChatSessionId.value === chatSessionId) {
    deleteChatSession(chatSessionId);
  }
};
</script>
