<template>
  <div>
    <div>
      Upload file:
      <input ref="fileInput" type="file" @change="handleFileInputChange()" />
      <button @click="handleFileUpload">Upload</button>
    </div>
    <pre v-if="uploading">Uploading...</pre>
    <pre style="color: green">{{ uploadMessage }}</pre>
    <pre style="color: red">{{ errorMessage }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const fileInput = ref<HTMLInputElement | null>(null);
// const files = ref<FileList | null>();

const uploadMessage = ref("");
const errorMessage = ref("");
const uploading = ref(false);

const handleFileInputChange = () => {
  uploadMessage.value = "";
  errorMessage.value = "";
};

const handleFileUpload = async () => {
  console.log("handleFileUpload", fileInput.value?.files);

  const files = fileInput.value?.files;
  if (files == null) {
    return;
  }
  const filesToUpload = Array.from(files);
  uploadFiles(filesToUpload);
};

const uploadFiles = async (files: File[]) => {
  uploadMessage.value = "";
  errorMessage.value = "";
  uploading.value = true;

  const formData = new FormData();
  formData.append("file", files[0], files[0].name);
  // files.forEach((file) => formData.append(file.name, file));

  try {
    const response = await fetch("/api/upsert-file", {
      method: "POST",
      body: formData,
    });

    if (response.status >= 400) {
      console.log("Error:", response);
      const message = {
        status: response.status,
        statusText: response.statusText,
        body: await response.text(),
      };
      throw new Error(JSON.stringify(message));
    }

    uploadMessage.value = await response.text();
  } catch (error) {
    console.error("Error:", error);
    errorMessage.value =
      error instanceof Error ? error.message : JSON.stringify(error);
  } finally {
    uploading.value = false;
  }
};
</script>
