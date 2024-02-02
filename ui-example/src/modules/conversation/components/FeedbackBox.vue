<template>
  <div
    v-if="items != null && items.length > 0"
    class="border rounded border-app-border px-4 py-3"
  >
    <div v-for="item in items" class="flex flex-col">
      <div class="whitespace-pre-line">
        {{ item.text }}
      </div>
      <div class="self-end opacity-50">
        {{ useTimeAgo(item.date).value }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTimeAgo } from "@vueuse/core";
import { FeedbackItem } from "../types";

defineProps<{
  items: FeedbackItem[] | null;
}>();
</script>
