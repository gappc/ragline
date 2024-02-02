<template>
  <div class="flex flex-col min-h-dvh h-dvh">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount } from "vue";
import { router } from "../routes";
import { useAuthStore } from "../modules/auth/authStore";

onBeforeMount(() => {
  // Redirect to login page if not authorized
  if (!useAuthStore().authorized) {
    router.replace({ name: "login" });
  }
});
</script>
