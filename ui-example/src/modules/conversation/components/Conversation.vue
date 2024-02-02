<template>
  <div class="flex flex-col gap-4 w-full md:w-[40rem] mt-6 mb-12">
    <div
      v-for="(item, index) in conversation.items"
      class="flex flex-col gap-6"
      :key="item.promptId ?? ''"
    >
      <Prompt :prompt="item.prompt" />
      <Answer
        :item="item"
        :is-last="index == conversation.items.length - 1"
        :loading="loading"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ConversationContext } from "../types";
import Answer from "./Answer.vue";
import Prompt from "./Prompt.vue";

defineProps<{ conversation: ConversationContext; loading: boolean }>();
</script>
