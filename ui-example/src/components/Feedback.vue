<template>
  <div class="flex gap-2">
    <button
      :disabled="queryId == null"
      :class="[{ 'opacity-50': sentiment !== 'good' }]"
      @click="setAndSendSentiment('good')"
    >
      👍
    </button>
    <button
      :disabled="queryId == null"
      :class="[{ 'opacity-50': sentiment !== 'bad' }]"
      @click="setAndSendSentiment('bad')"
    >
      👎
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { client } from "../modules/api/client";

const props = defineProps<{ queryId?: string | null }>();

type Sentiment = "none" | "good" | "bad";

const sentiment = ref<Sentiment>("none");

const setAndSendSentiment = async (newValue: Sentiment) => {
  // Unset sentiment if it's already set
  sentiment.value = sentiment.value === newValue ? "none" : newValue;

  // Don't send sentiment if queryId is undefined
  if (props.queryId == null) {
    console.warn("queryId is undefined");
    return;
  }

  const response = await client("/api/feedback/sentiment/" + props.queryId, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sentiment: sentiment.value,
    }),
  });
  console.log("response", response);
};
</script>
