<template>
  <div class="flex gap-3">
    <div class="bg-white rounded-full h-7 w-7"></div>
    <div class="flex flex-col flex-1 gap-1">
      <span class="font-bold">HUG-GPT</span>

      <!-- Show loading info-->
      <div
        v-if="loading && (item.answer?.length ?? 0) === 0"
        class="text-gray-500 animate-pulse"
      >
        Loading...
      </div>

      <!-- Show answer -->
      <div v-if="item.answer">{{ item.answer }}</div>

      <!-- Document sources -->
      <div v-if="item.sources.length > 0" class="flex flex-col divide-y mt-3">
        <div class="font-bold py-3">Documents that were searched</div>
        <div v-for="source in item.sources" class="flex justify-between py-3">
          <a :href="`/api/files/${source.file}`">{{ source.file }}</a>
          <span>Pages ({{ source.pages.join(",") }})</span>
        </div>
      </div>

      <!-- Show feedback -->
      <Feedback
        v-if="item.promptId != null && (isLast || item.feedback != null)"
        class="mt-2"
        :prompt-id="item.promptId"
        :sentiment="item.feedback?.sentiment ?? null"
        :items="item.feedback?.items ?? null"
        :editable="isLast"
        :loading="loading"
      />

      <!-- Show error -->
      <div v-if="item.error != null" class="text-error">
        {{ item.error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ConversationItem } from "../types";
import Feedback from "./Feedback.vue";

defineProps<{ item: ConversationItem; isLast: boolean; loading: boolean }>();
</script>
