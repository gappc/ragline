import { acceptHMRUpdate, defineStore } from "pinia";

interface State {
  message: string | null;
  type: "info" | "success" | "error" | null;
}

const initialState: State = {
  message: null,
  type: null,
};

export const useMessageStore = defineStore("messageStore", {
  state: () => initialState,
  actions: {
    setInfo(message: string) {
      this.message = message;
      this.type = "info";
    },
    setSuccess(message: string) {
      this.message = message;
      this.type = "success";
    },
    setError(message: string) {
      this.message = message;
      this.type = "error";
    },
    reset() {
      this.message = null;
      this.type = null;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMessageStore, import.meta.hot));
}
