<template>
  <div class="flex items-center border gap-3 px-3">
    <slot name="prepend"></slot>
    <input
      v-model="model"
      class="grow py-4 my-px"
      :type="type"
      :placeholder="placeholder"
      :autocomplete="autocomplete"
      :autofocus="autofocus"
      @keyup.enter="emit('keyup.enter', $event)"
    />
    <slot name="append"></slot>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: string;
    placeholder?: string;
    autocomplete?: string;
    autofocus?: boolean;
  }>(),
  {
    type: "text",
    placeholder: undefined,
    autocomplete: undefined,
    autofocus: undefined,
  }
);

const model = defineModel();

const emit = defineEmits(["keyup.enter"]);
</script>
