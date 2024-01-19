<template>
  <div>
    <h2>Files</h2>
    <button @click="fetchFileList">Load File List</button>
    <div>
      <div
        v-for="file in files"
        style="
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 1rem;
        "
      >
        <div style="width: 40rem; text-align: left">{{ file.name }}</div>
        <div>
          <span>{{ file.size / 1e6 }} MB</span>
          <button @click="deleteFile(file.name)">Delete</button>
        </div>
      </div>
    </div>
    <div v-if="fileListLoading">Loading...</div>
    <div v-if="fileListMessage" style="color: green">
      {{ fileListMessage }}
    </div>
    <div v-if="fileListError" style="color: red">{{ fileListError }}</div>

    <div v-if="deleteFileLoading">Deleting...</div>
    <div v-if="deleteFileMessage" style="color: green">
      {{ deleteFileMessage }}
    </div>
    <div v-if="deleteFileError" style="color: red">{{ deleteFileError }}</div>
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
