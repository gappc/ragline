<template>
  <div>
    <div>
      Upload file:
      <input ref="fileInput" type="file" @change="handleFileUpload()" />
    </div>
    <pre>{{ uploadMessage }}</pre>
    <pre style="color: red">{{ errorMessage }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const fileInput = ref<HTMLInputElement | null>(null);
// const files = ref<FileList | null>();

const uploadMessage = ref("");
const errorMessage = ref("");

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

  const formData = new FormData();
  formData.append("file", files[0], files[0].name);
  // files.forEach((file) => formData.append(file.name, file));

  fetch("/api/upsert-file", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.status >= 400) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then((result) => {
      console.log("Success:", result);
      uploadMessage.value = JSON.stringify(result);
    })
    .catch((error) => {
      console.error("Error:", error);
      uploadMessage.value = JSON.stringify(error);
    });
};
</script>
