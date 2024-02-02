<template>
  <div class="flex items-center border gap-3 px-3">
    <slot name="prepend"></slot>
    <input
      ref="inputElement"
      v-model="model"
      class="grow py-4 my-px"
      :type="type"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      :autofocus="autofocus"
      @keyup.enter="emit('keyup.enter', $event)"
    />
    <ButtonCustom
      v-if="withResetButton"
      size="xs"
      variant="ghost"
      class="p-1 border-0"
      :class="model?.length === 0 ? 'hidden' : ''"
      :disabled="model?.length === 0"
      @click="reset"
    >
      <IconClose class="w-6 h-6" />
    </ButtonCustom>
    <slot name="append"></slot>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ButtonCustom from "../button/ButtonCustom.vue";
import IconClose from "../svg/IconClose.vue";

withDefaults(
  defineProps<{
    type?: string;
    placeholder?: string;
    autocomplete?: string;
    autofocus?: boolean;
    withResetButton?: boolean;
  }>(),
  {
    type: "text",
    placeholder: undefined,
    autocomplete: undefined,
    autofocus: undefined,
    withResetButton: false,
  }
);

const model = defineModel<string>();

const emit = defineEmits(["keyup.enter"]);

const inputElement = ref<HTMLInputElement | null>(null);

const reset = () => {
  model.value = "";
  inputElement.value?.focus();
};
</script>
