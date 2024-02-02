<template>
  <div class="flex flex-col gap-2">
    <div class="flex gap-2">
      <IconThumbUp
        v-if="sentiment === 'good'"
        class="w-8 h-8 p-2 bg-white fill-app-bg"
      />
      <IconThumbDown
        v-if="sentiment === 'bad'"
        class="w-8 h-8 p-2 bg-white fill-app-bg"
      />
    </div>

    <FeedbackBox :items="items" />
  </div>
</template>

<script setup lang="ts">
import IconThumbDown from "../../../components/svg/IconThumbDown.vue";
import IconThumbUp from "../../../components/svg/IconThumbUp.vue";
import { FeedbackItem, Sentiment } from "../types";
import FeedbackBox from "./FeedbackBox.vue";

defineProps<{
  promptId: string | null;
  sentiment: Sentiment | null;
  items: FeedbackItem[] | null;
}>();
</script>
