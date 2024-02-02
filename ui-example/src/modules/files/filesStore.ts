import { acceptHMRUpdate, defineStore } from "pinia";
import { client } from "../api/client";
import { errorToMessage } from "../api/responseError";
import { FileEntry } from "./types";
import { useMessageStore } from "../messages/messageStore";

interface State {
  files: FileEntry[];
  fileListLoading: boolean;
  uploadFileLoading: boolean;
  deleteFileLoading: boolean;
  uploadAbortController: AbortController | null;
}

const initialState: State = {
  files: [],
  fileListLoading: false,
  uploadFileLoading: false,
  deleteFileLoading: false,
  uploadAbortController: null,
};

export const useFileStore = defineStore("filesStore", {
  state: () => initialState,
  actions: {
    async fetchFiles() {
      this.files = [];
      this.fileListLoading = true;

      try {
        const response = await client("/api/files");
        this.files = await response.json();
      } catch (error) {
        useMessageStore().setError(errorToMessage(error));
      } finally {
        this.fileListLoading = false;
      }
    },
    async uploadFiles(files: File[]) {
      useMessageStore().setInfo("Uploading");
      this.uploadFileLoading = true;

      // Handle aborting the previous request
      if (
        this.uploadAbortController != null &&
        !this.uploadAbortController.signal.aborted
      ) {
        this.uploadAbortController.abort();
      }
      this.uploadAbortController = new AbortController();

      const formData = new FormData();
      files.forEach((file) => formData.append("files", file, file.name));

      try {
        await client("/api/files", {
          method: "POST",
          body: formData,
        });
        useMessageStore().setSuccess("Upload success");
      } catch (error) {
        useMessageStore().setError(errorToMessage(error));
      } finally {
        this.uploadFileLoading = false;
      }
    },
    async deleteFile(filename: string) {
      this.deleteFileLoading = true;

      try {
        await client(`/api/files/${filename}`, { method: "DELETE" });
        useMessageStore().setSuccess(`Delete file ${filename} success`);
      } catch (error) {
        useMessageStore().setError(errorToMessage(error));
      } finally {
        this.deleteFileLoading = false;
      }
    },
    reset() {
      this.files = [];
      this.fileListLoading = false;
      this.uploadFileLoading = false;
      this.deleteFileLoading = false;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useFileStore, import.meta.hot));
}
