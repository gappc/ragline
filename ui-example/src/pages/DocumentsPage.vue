<template>
  <MainLayout>
    <div class="flex flex-col flex-1 justify-between divide-y overflow-y-auto">
      <div
        ref="scrollWindow"
        class="flex flex-col items-center overflow-y-auto"
      >
        <Files />
      </div>
      <div class="py-6 flex justify-center">
        <FileUpload />
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from "../layouts/MainLayout.vue";
import Files from "../modules/files/components.ts/Files.vue";
import FileUpload from "../modules/files/components.ts/FileUpload.vue";
</script>
