<template>
  <InputCustom
    v-model="model"
    placeholder="Type here your questions..."
    class="w-full md:w-[40rem]"
    @keyup.enter="emit('submit', model)"
  >
    <template #append>
      <ButtonCustom
        v-if="!loading"
        class="p-1"
        size="xs"
        :disabled="model?.length === 0"
        @click="emit('submit', model)"
      >
        <IconArrowUpwardAlt class="bg-transparent fill-app-bg" />
      </ButtonCustom>
      <ButtonCustom
        v-else
        size="xs"
        variant="ghost"
        class="border-0"
        @click="abortController?.abort()"
      >
        <IconStop class="w-10 h-10" />
      </ButtonCustom>
    </template>
  </InputCustom>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ButtonCustom from "../button/ButtonCustom.vue";
import IconArrowUpwardAlt from "../svg/IconArrowUpwardAlt.vue";
import IconStop from "../svg/IconStop.vue";
import InputCustom from "./InputCustom.vue";

withDefaults(
  defineProps<{
    loading: boolean;
    abortController: AbortController | null;
  }>(),
  {
    abortController: null,
  }
);

const model = ref<string>("");

const emit = defineEmits(["submit"]);
</script>
