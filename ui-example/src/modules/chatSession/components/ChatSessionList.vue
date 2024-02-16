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
        <ButtonDeleteWithApprove
          @delete="deleteChatSession(chatSession.chatSessionId)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDateFormat } from "@vueuse/core";
import { storeToRefs } from "pinia";
import ButtonCustom from "../../../components/button/ButtonCustom.vue";
import ButtonDeleteWithApprove from "../../../components/button/ButtonDeleteWithApprove.vue";
import { useChatSessionStore } from "../chatSessionStore";

const { chatSessions, currentChatSessionId } = storeToRefs(
  useChatSessionStore()
);

const { setCurrentChatSession, deleteChatSession } = useChatSessionStore();
</script>
