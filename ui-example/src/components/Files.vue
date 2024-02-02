<template>
  <div class="border rounded p-2">
    <h2>Files</h2>
    <div class="flex flex-col gap-1 max-h-80 overflow-y-auto py-4">
      <div v-for="file in files" class="flex justify-between items-center">
        <a
          :href="`/api/files/${file.name}`"
          target="_blank"
          class="overflow-auto"
          >{{ file.name }}</a
        >
        <div class="flex items-center gap-2">
          <span>{{ Math.round(file.size / 1e3) / 1e3 }} MB</span>
          <button @click="deleteFile(file.name)">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useFileStore } from "../modules/files/filesStore";
import { onBeforeMount } from "vue";

const { files } = storeToRefs(useFileStore());

const deleteFile = async (fileName: string) => {
  await useFileStore().deleteFile(fileName);
  await useFileStore().fetchFiles();
};

onBeforeMount(() => useFileStore().fetchFiles());
</script>
