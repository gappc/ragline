<template>
  <div class="border rounded p-2">
    <h2>Files</h2>
    <button @click="fetchFileList">Load File List</button>
    <div class="flex flex-col gap-1 max-h-80 overflow-y-auto py-4">
      <div v-for="file in files" class="flex justify-between items-center">
        <a
          :href="`/api/files/${file.name}`"
          target="_blank"
          class="text-left"
          >{{ file.name }}</a
        >
        <div class="flex items-center gap-2">
          <span>{{ Math.round(file.size / 1e3) / 1e3 }} MB</span>
          <button @click="deleteFile(file.name)">Delete</button>
        </div>
      </div>
    </div>
    <div v-if="fileListLoading">Loading...</div>
    <div v-if="fileListMessage" class="text-success">
      {{ fileListMessage }}
    </div>
    <div v-if="fileListError" class="text-error">{{ fileListError }}</div>

    <div v-if="deleteFileLoading">Deleting...</div>
    <div v-if="deleteFileMessage" class="text-success">
      {{ deleteFileMessage }}
    </div>
    <div v-if="deleteFileError" class="text-error">{{ deleteFileError }}</div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useFileStore } from "../modules/files/filesStore";

const {
  files,
  deleteFileError,
  deleteFileLoading,
  deleteFileMessage,
  fileListError,
  fileListLoading,
  fileListMessage,
} = storeToRefs(useFileStore());

const { fetchFileList, deleteFile } = useFileStore();
</script>
