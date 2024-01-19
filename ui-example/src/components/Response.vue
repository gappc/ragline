<template>
  <div>
    Full response:
    <pre>{{ response }}</pre>
  </div>
</template>

<script setup lang="ts">
import { toRefs, watch } from "vue";

const props = defineProps<{ response: unknown }>();

const { response } = toRefs(props);

watch(response, (response) => {
  console.log(response);
});
</script>
