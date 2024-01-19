<template>
  <div style="display: flex; flex-direction: column; gap: 2rem">
    <Files />
    <Upload />
    <Query />
  </div>
</template>

<script setup lang="ts">
import Files from "./components/Files.vue";
import Query from "./components/Query.vue";
import Upload from "./components/Upload.vue";
import { useFileStore } from "./modules/files/filesStore";

useFileStore().fetchFileList();
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
