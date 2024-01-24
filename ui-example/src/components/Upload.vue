<template>
  <div>
    <div>
      <h2>Upload file</h2>
      <input ref="fileInput" type="file" multiple @change="computeHasFiles" />
      <button
        @click="handleFileUpload"
        :disabled="!hasFiles"
        :class="[{ 'opacity-50': !hasFiles }]"
      >
        Upload
      </button>
      <span class="ml-5 opacity-50">
        This may take some time, please be patient
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useFileStore } from "../modules/files/filesStore";

const fileInput = ref<HTMLInputElement | null>(null);

const hasFiles = ref(false);

const computeHasFiles = () => {
  const files = fileInput.value?.files;
  hasFiles.value = files != null && Object.keys(files).length > 0;
};

const handleFileUpload = async () => {
  const files = fileInput.value?.files;

  if (!hasFiles) {
    console.log("No files selected");
    return;
  }

  const filesToUpload = Array.from(files!);
  console.time("upload");
  await useFileStore().uploadFiles(filesToUpload);
  console.timeEnd("upload");
  await useFileStore().fetchFiles();
};
</script>
