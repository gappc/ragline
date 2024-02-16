<template>
  <ButtonCustom size="xs" variant="ghost" class="p-2" @click="statefulEmit">
    <IconDelete v-if="!showApproval" class="w-4 h-4 fill-red-500" />
    <IconThumbUp v-else class="w-4 h-4 fill-red-500" />
  </ButtonCustom>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ButtonCustom from "./ButtonCustom.vue";
import IconDelete from "../svg/IconDelete.vue";
import IconThumbUp from "../svg/IconThumbUp.vue";

const emit = defineEmits(["delete"]);

const showApproval = ref(false);

const statefulEmit = async () => {
  if (!showApproval.value) {
    showApproval.value = true;
    setTimeout(() => (showApproval.value = false), 3000);
  } else {
    showApproval.value = false;
    emit("delete");
  }
};
</script>
