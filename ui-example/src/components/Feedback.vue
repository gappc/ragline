<template>
  <div class="flex flex-col gap-7">
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
    <div v-for="feedback in feedbacks" class="flex flex-col gap-2 text-left">
      <div class="border rounded border-slate-500 px-4 py-3">
        {{ feedback.text }}
      </div>
      <div class="self-end opacity-50">
        {{ useTimeAgo(feedback.date).value }}
      </div>
    </div>
    <div>
      <textarea
        class="w-full"
        rows="3"
        placeholder="Feedback"
        v-model="feedback"
      ></textarea>
      <button class="w-2/4" @click="sendFeedback">Send</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useMagicKeys, useTimeAgo } from "@vueuse/core";
import { client } from "../modules/api/client";

const props = defineProps<{ queryId?: string | null }>();

type Sentiment = "none" | "good" | "bad";

const sentiment = ref<Sentiment>("none");
const feedback = ref<string>("");
const feedbacks = ref<{ text: string; date: Date }[]>([]);

const setAndSendSentiment = async (newValue: Sentiment) => {
  // Unset sentiment if it's already set
  sentiment.value = sentiment.value === newValue ? "none" : newValue;

  // Don't send sentiment if queryId is undefined
  if (props.queryId == null) {
    console.warn("queryId is undefined");
    return;
  }

  const response = await client("/api/sentiment/" + props.queryId, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sentiment: sentiment.value,
    }),
  });
  console.log("response", response);
};

const sendFeedback = async () => {
  // Don't send feedback if queryId is undefined
  if (props.queryId == null) {
    console.warn("queryId is undefined");
    return;
  }

  if (feedback.value === "") {
    console.warn("feedback is empty");
    return;
  }

  const response = await client("/api/feedback/" + props.queryId, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      feedback: feedback.value,
    }),
  });
  console.log("response", response);

  feedbacks.value = [
    ...feedbacks.value,
    { text: feedback.value, date: new Date() },
  ];
};

const keys = useMagicKeys();
const shiftCtrlA = keys["Ctrl+Enter"];

watch(shiftCtrlA, (key) => {
  if (key) {
    sendFeedback();
  }
});
</script>
