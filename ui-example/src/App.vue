<template>
  <div class="flex flex-col gap-4">
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
