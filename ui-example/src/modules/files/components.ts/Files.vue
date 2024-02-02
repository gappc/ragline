<template>
  <div class="flex flex-col gap-4 w-full md:w-[40rem] mt-6 mb-12">
    <InputCustom
      v-model="searchFileName"
      ref="searchInput"
      placeholder="Search your document ..."
      class="w-full"
      autofocus
      :with-reset-button="true"
    >
      <template #append>
        <ButtonCustom
          size="xs"
          class="p-1"
          :disabled="searchFileName.length === 0"
        >
          <IconSearch class="w-6 h-6 bg-white" />
        </ButtonCustom>
      </template>
    </InputCustom>
    <div class="flex flex-col max-h-80 overflow-y-auto py-4 divide-y">
      <div
        v-for="file in filteredFiles"
        class="flex justify-between items-center p-2"
      >
        <a
          :href="`/api/files/${file.name}`"
          target="_blank"
          class="overflow-auto"
        >
          {{ file.name }}
        </a>
        <div class="flex items-center gap-2">
          <ButtonCustom size="xs" variant="ghost" class="p-2">
            <IconPushPin class="w-4 h-4 fill-white" />
          </ButtonCustom>
          <ButtonCustom size="xs" variant="ghost" class="p-2">
            <IconDelete
              class="w-4 h-4 fill-red-500"
              @click="deleteFile(file.name)"
            />
          </ButtonCustom>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, onBeforeMount, ref } from "vue";
import ButtonCustom from "../../../components/button/ButtonCustom.vue";
import InputCustom from "../../../components/input/InputCustom.vue";
import IconSearch from "../../../components/svg/IconSearch.vue";
import { useFileStore } from "../filesStore";
import { FileEntry } from "../types";
import IconPushPin from "../../../components/svg/IconPushPin.vue";
import IconDelete from "../../../components/svg/IconDelete.vue";

const searchFileName = ref("");

const { files } = storeToRefs(useFileStore());

const filteredFiles = computed<FileEntry[]>(() => {
  if (searchFileName.value === "") {
    return files.value;
  }

  const upperCaseSearchFileName = searchFileName.value.toUpperCase();

  return files.value.filter((file) =>
    file.name.toLocaleUpperCase().includes(upperCaseSearchFileName)
  );
});

const deleteFile = async (fileName: string) => {
  await useFileStore().deleteFile(fileName);
  await useFileStore().fetchFiles();
};

onBeforeMount(() => useFileStore().fetchFiles());
</script>
