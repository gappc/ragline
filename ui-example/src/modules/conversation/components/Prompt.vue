<template>
  <div class="flex gap-3">
    <div class="bg-white rounded-full h-7 w-7"></div>
    <div class="flex flex-col flex-1 gap-1">
      <span class="font-bold">DU</span>
      <span>{{ prompt }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ prompt: string }>();
</script>
