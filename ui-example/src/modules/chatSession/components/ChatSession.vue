<template>
  <div class="flex flex-col gap-4 w-full md:w-[40rem] mt-6 mb-12">
    <div
      v-for="(event, index) in chatSession.events"
      class="flex flex-col gap-6"
      :key="event.promptId ?? ''"
    >
      <Prompt :prompt="event.prompt" />
      <Answer
        :event="event"
        :is-last="index == chatSession.events.length - 1"
        :loading="loading"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChatSession } from "../types";
import Answer from "./Answer.vue";
import Prompt from "./Prompt.vue";

defineProps<{ chatSession: ChatSession; loading: boolean }>();
</script>
