<template>
  <button :class="classes" :disabled="disabled">
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { toRefs } from "vue";
import { useButtonClasses } from "./styles";
import { Size, Tone, Variant } from "./types";

const props = withDefaults(
  defineProps<{
    size?: Size;
    tone?: Tone;
    variant?: Variant;
    disabled?: boolean;
  }>(),
  {
    size: "md",
    tone: "primary",
    variant: "solid",
    disabled: false,
  }
);

const { size, tone, variant, disabled } = toRefs(props);

const classes = useButtonClasses({ size, tone, variant, disabled });
</script>
