<template>
  <div class="flex flex-col gap-4">
    <Login />
    <Messages />
    <Files v-if="authorized" />
    <Upload v-if="authorized" />
    <Query v-if="authorized" />
  </div>
</template>

<script setup lang="ts">
import Files from "./components/Files.vue";
import Query from "./components/Query.vue";
import Upload from "./components/Upload.vue";
import Login from "./components/Login.vue";
import { useAuthStore } from "./modules/auth/authStore";
import { storeToRefs } from "pinia";
import Messages from "./components/Messages.vue";

const { authorized } = storeToRefs(useAuthStore());
</script>
