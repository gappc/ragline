<template>
  <div>
    <OldFeedback
      v-if="!editable"
      :prompt-id="promptId"
      :sentiment="sentiment"
      :items="items"
    />
    <NewFeedback
      v-if="editable && !loading"
      :prompt-id="promptId"
      :sentiment="sentiment"
      :items="items"
    />
  </div>
</template>

<script setup lang="ts">
import { FeedbackItem, Sentiment } from "../types";
import NewFeedback from "./NewFeedback.vue";
import OldFeedback from "./OldFeedback.vue";

defineProps<{
  promptId: string | null;
  sentiment: Sentiment | null;
  items: FeedbackItem[] | null;
  editable: boolean;
  loading: boolean;
}>();
</script>
