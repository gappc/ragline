<template>
  <div class="w-full md:w-[40rem]">
    <div
      class="border-2 border-dotted"
      :class="{ 'border-success-700': isOverDropZone }"
    >
      <ButtonCustom
        v-if="!uploadFileLoading"
        ref="dropZoneRef"
        size="xs"
        variant="ghost"
        class="flex justify-between items-center w-full border-0 my-[2px] px-3"
        @click="open"
      >
        <div class="py-4">Wähle Deine Dateien aus</div>
        <div class="bg-white">
          <div class="p-1 bg-white" size="xs">
            <IconArrowUpwardAlt class="bg-transparent fill-app-bg" />
          </div>
        </div>
      </ButtonCustom>
      <div v-else class="flex justify-between items-center px-2">
        <div></div>
        <div class="py-4 animate-pulse">Uploading and indexing...</div>
        <ButtonCustom
          size="xs"
          variant="ghost"
          class="border-0"
          @click="uploadAbortController?.abort()"
        >
          <IconStop class="w-10 h-10" />
        </ButtonCustom>
      </div>
    </div>

    <div class="text-center">
      {{ useMessageStore().type === "error" ? useMessageStore().message : "" }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import ButtonCustom from "../../../components/button/ButtonCustom.vue";
import IconArrowUpwardAlt from "../../../components/svg/IconArrowUpwardAlt.vue";
import { useDropZone, useFileDialog } from "@vueuse/core";
import { useFileStore } from "../filesStore";
import { storeToRefs } from "pinia";
import IconStop from "../../../components/svg/IconStop.vue";
import { useMessageStore } from "../../messages/messageStore";

const fileNames = ref<string[]>([]);

const onDrop = (filesFromDropZone: File[] | null) => {
  if (filesFromDropZone == null) {
    return;
  }

  // Check if all files have the correct file type. This check is done here
  // because the drag & drop file selection does not support file type filters
  //   const notAccepted = filesFromDropZone.filter(
  //     (file) => !isFileTypeAccepted(props.type, file.type)
  //   );
  //   if (notAccepted.length > 0) {
  //     fileTypesNotAccepted.value = {
  //       title: `Some file have file types that are not accepted (accepted: ${props.type})`,
  //       content: notAccepted.map((f) => f.name).join(", "),
  //     };
  //     return;
  //   }

  //   fileTypesNotAccepted.value = undefined;

  fileNames.value = filesFromDropZone.map((item) => item.name);

  uploadInternal(filesFromDropZone);
};

const dropZoneRef = ref<HTMLDivElement>();
const { isOverDropZone } = useDropZone(dropZoneRef, onDrop);

const { files, open, reset } = useFileDialog({
  multiple: true,
  accept: "application/pdf",
});

watch(files, (filesFromFileDialog) => {
  if (filesFromFileDialog == null) {
    return;
  }

  const filesToUpload = Array.from(filesFromFileDialog);
  fileNames.value = filesToUpload.map((item) => item.name);

  // Trigger file upload
  uploadInternal(filesToUpload);
});

const { fetchFiles, uploadFiles } = useFileStore();
const { uploadAbortController, uploadFileLoading } = storeToRefs(
  useFileStore()
);

const uploadInternal = async (files: File[]) => {
  console.log("uploading", files);
  console.time("upload");
  await uploadFiles(files);
  console.timeEnd("upload");
  reset();
  await fetchFiles();
};
</script>
