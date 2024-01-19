import { acceptHMRUpdate, defineStore } from "pinia";
import { FileEntry } from "./types";

interface State {
  files: FileEntry[];
  fileListLoading: boolean;
  fileListMessage: string | undefined | null;
  fileListError: string | undefined | null;
  uploadFileLoading: boolean;
  uploadFileMessage: string | undefined | null;
  uploadFileError: string | undefined | null;
  deleteFileLoading: boolean;
  deleteFileMessage: string | undefined | null;
  deleteFileError: string | undefined | null;
}

const initialState: State = {
  files: [],
  fileListLoading: false,
  fileListMessage: null,
  fileListError: null,
  uploadFileLoading: false,
  uploadFileMessage: null,
  uploadFileError: null,
  deleteFileLoading: false,
  deleteFileMessage: null,
  deleteFileError: null,
};

export const useFileStore = defineStore("filesStore", {
  state: () => initialState,
  actions: {
    async fetchFileList() {
      this.fileListLoading = true;
      this.clearMessages();

      try {
        const response = await fetch("/api/files");

        if (response.status >= 400) {
          console.log("Error:", response);
          const message = {
            status: response.status,
            statusText: response.statusText,
            body: await response.text(),
          };
          throw new Error(JSON.stringify(message));
        }

        this.files = await response.json();
        this.fileListMessage = "Load file list success";
      } catch (error) {
        this.fileListError =
          error instanceof Error ? error.message : JSON.stringify(error);
      } finally {
        this.fileListLoading = false;
      }
    },
    async uploadFiles(files: File[]) {
      this.uploadFileLoading = true;
      this.clearMessages();

      const formData = new FormData();
      files.forEach((file) => formData.append("files", file, file.name));

      try {
        const response = await fetch("/api/files", {
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

        this.uploadFileMessage = await response.text();
      } catch (error) {
        this.uploadFileError =
          error instanceof Error ? error.message : JSON.stringify(error);
      } finally {
        this.uploadFileLoading = false;
      }
    },
    async deleteFile(filename: string) {
      this.deleteFileLoading = true;
      this.clearMessages();

      try {
        const response = await fetch(`/api/files/${filename}`, {
          method: "DELETE",
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
        this.deleteFileMessage = `Delete file ${filename} success`;
      } catch (error) {
        this.deleteFileError =
          error instanceof Error ? error.message : JSON.stringify(error);
      } finally {
        this.deleteFileLoading = false;
      }

      this.fetchFileList();
    },
    clearMessages() {
      this.fileListMessage = null;
      this.fileListError = null;
      this.uploadFileMessage = null;
      this.uploadFileError = null;
      this.deleteFileMessage = null;
      this.deleteFileError = null;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useFileStore, import.meta.hot));
}
