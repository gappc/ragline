<template>
  <div>
    <div
      v-if="message"
      class="flex justify-between items-start"
      :class="classes"
    >
      <div class="p-2 break-words">{{ message }}</div>
      <button @click="useMessageStore().reset()">x</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useMessageStore } from "../modules/messages/messageStore";
import { computed } from "vue";

const { message, type } = storeToRefs(useMessageStore());

const classes = computed(() => {
  switch (type.value) {
    case "success":
      return "bg-green-500";
    case "error":
      return "bg-red-500";
    default:
      return "";
  }
});
</script>
