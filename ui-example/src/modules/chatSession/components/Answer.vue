<template>
  <div class="flex gap-3">
    <div class="bg-white rounded-full h-7 w-7"></div>
    <div class="flex flex-col flex-1 gap-1">
      <span class="font-bold">HUG-GPT</span>

      <!-- Show loading info-->
      <div
        v-if="loading && (event.answer?.length ?? 0) === 0"
        class="text-gray-500 animate-pulse"
      >
        Loading...
      </div>

      <!-- Show answer -->
      <div v-if="event.answer">{{ event.answer }}</div>

      <!-- Document sources -->
      <div v-if="event.sources.length > 0" class="flex flex-col divide-y mt-3">
        <div class="font-bold py-3">Documents that were searched</div>
        <div v-for="source in event.sources" class="flex justify-between py-3">
          <a :href="`/api/files/${source.file}`" target="_blank">{{
            source.file
          }}</a>
          <span>Pages ({{ source.pages.join(",") }})</span>
        </div>
      </div>

      <!-- Show feedback -->
      <Feedback
        v-if="event.promptId != null && (isLast || event.feedback != null)"
        class="mt-2"
        :prompt-id="event.promptId"
        :sentiment="event.feedback?.sentiment ?? null"
        :items="event.feedback?.items ?? null"
        :editable="isLast"
        :loading="loading"
      />

      <!-- Show error -->
      <div v-if="event.error != null" class="text-error">
        {{ event.error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChatEvent } from "../types";
import Feedback from "./Feedback.vue";

defineProps<{ event: ChatEvent; isLast: boolean; loading: boolean }>();
</script>
