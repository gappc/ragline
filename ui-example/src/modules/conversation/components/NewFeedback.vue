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

    <div
      v-if="showFeedbackThankYou"
      class="flex items-center gap-3 mx-2 md:mx-0 p-2 mt-3 bg-success-500 text-success-700 fill-success-700 outline outline-white outline-2 outline-offset-4"
    >
      <IconMood class="w-8 h-8 bg-success-500 fill-success-700" />
      Thanks for your feedback!
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMagicKeys, useTextareaAutosize } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";
import ButtonCustom from "../../../components/button/ButtonCustom.vue";
import IconMood from "../../../components/svg/IconMood.vue";
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

const showFeedbackThankYou = ref(false);

const { textarea, input } = useTextareaAutosize();

const { currentConversationId, currentItems } = storeToRefs(
  useConversationStore()
);

const sendSentimentInternal = async (sentiment: Sentiment) => {
  const success = await sendSentiment(
    currentConversationId.value,
    props.promptId,
    currentItems.value,
    sentiment === props.sentiment ? "none" : sentiment
  );

  if (success) {
    showFeedbackThankYouInternal();
  }
};

const sendFeedbackInternal = async () => {
  const success = await sendFeedback(
    currentConversationId.value,
    props.promptId,
    currentItems.value,
    input.value
  );
  input.value = "";

  if (success) {
    showFeedbackThankYouInternal();
  }
};

const showFeedbackThankYouInternal = () => {
  showFeedbackThankYou.value = true;
  setTimeout(() => (showFeedbackThankYou.value = false), 3000);
};

const keys = useMagicKeys();
const shiftCtrlA = keys["Ctrl+Enter"];

watch(shiftCtrlA, (key) => {
  if (key) {
    sendFeedbackInternal();
  }
});
</script>
