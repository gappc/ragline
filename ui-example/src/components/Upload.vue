<template>
  <div>
    <div>
      <h2>Upload file</h2>
      <input ref="fileInput" type="file" multiple @change="handleFileUpload" />
      <button @click="handleFileUpload">Upload</button>
    </div>
    <div v-if="uploadFileLoading">Uploading...</div>
    <div v-if="uploadFileMessage" style="color: green">
      {{ uploadFileMessage }}
    </div>
    <div v-if="uploadFileError" style="color: red">{{ uploadFileError }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useFileStore } from "../modules/files/filesStore";

const fileInput = ref<HTMLInputElement | null>(null);

const { uploadFileMessage, uploadFileError, uploadFileLoading } = storeToRefs(
  useFileStore()
);

const handleFileUpload = async () => {
  console.log("handleFileUpload", fileInput.value?.files);

  const files = fileInput.value?.files;
  if (files == null) {
    return;
  }
  const filesToUpload = Array.from(files);
  await useFileStore().uploadFiles(filesToUpload);
  await useFileStore().fetchFileList();
};
</script>
