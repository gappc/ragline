<template>
  <div class="flex flex-col gap-2">
    <div class="flex gap-2">
      <ButtonCustom
        size="xs"
        variant="ghost"
        @click="sendSentimentInternal('good')"
      >
        <IconThumbUp
          class="w-8 h-8 p-2"
          :class="[
            sentiment === 'good' ? 'bg-white fill-app-bg' : 'fill-white border',
          ]"
        />
      </ButtonCustom>
      <ButtonCustom
        size="xs"
        variant="ghost"
        @click="sendSentimentInternal('bad')"
      >
        <IconThumbDown
          class="w-8 h-8 p-2"
          :class="[
            sentiment === 'bad' ? 'bg-white fill-app-bg' : 'fill-white border',
          ]"
        />
      </ButtonCustom>
    </div>

    <FeedbackBox :items="items" />

    <div class="flex flex-col gap-2">
      <textarea
        ref="textarea"
        class="w-full border p-2 resize-none min-h-10"
        rows="3"
        placeholder="Feedback"
        v-model="input"
      ></textarea>
      <ButtonCustom
        class="md:w-1/2"
        size="sm"
        variant="ghost"
        :disabled="input.length === 0"
        @click="sendFeedbackInternal"
      >
        Send feedback
      </ButtonCustom>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMagicKeys, useTextareaAutosize } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { watch } from "vue";
import ButtonCustom from "../../../components/button/ButtonCustom.vue";
import IconThumbDown from "../../../components/svg/IconThumbDown.vue";
import IconThumbUp from "../../../components/svg/IconThumbUp.vue";
import { useConversationStore } from "../conversationStore";
import { FeedbackItem, Sentiment } from "../types";
import { sendFeedback, sendSentiment } from "../useFeedback";
import FeedbackBox from "./FeedbackBox.vue";

const props = defineProps<{
  promptId: string | null;
  sentiment: Sentiment | null;
  items: FeedbackItem[] | null;
}>();

const { textarea, input } = useTextareaAutosize();

const { currentConversationId, currentItems } = storeToRefs(
  useConversationStore()
);

const sendSentimentInternal = async (sentiment: Sentiment) => {
  await sendSentiment(
    currentConversationId.value,
    props.promptId,
    currentItems.value,
    sentiment === props.sentiment ? "none" : sentiment
  );
};

const sendFeedbackInternal = async () => {
  await sendFeedback(
    currentConversationId.value,
    props.promptId,
    currentItems.value,
    input.value
  );
  input.value = "";
};

const keys = useMagicKeys();
const shiftCtrlA = keys["Ctrl+Enter"];

watch(shiftCtrlA, (key) => {
  if (key) {
    sendFeedbackInternal();
  }
});
</script>
