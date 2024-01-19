import { acceptHMRUpdate, defineStore } from "pinia";
import { client } from "../api/client";
import { errorToMessage } from "../api/responseError";
import { useMessageStore } from "../messages/messageStore";

interface State {
  token: string | null;
  username: string | null;
  authorized: boolean;
}

const initialState: State = {
  token: null,
  username: null,
  authorized: false,
};

export const useAuthStore = defineStore("authStore", {
  state: () => initialState,
  getters: {
    basicAuthHeader(state): Record<string, string> {
      return {
        Authorization: "Basic " + btoa(`${state.username}:${state.token}`),
      };
    },
  },
  actions: {
    buildBasicAuthHeader(username: string, token: string) {
      return { Authorization: "Basic " + btoa(`${username}:${token}`) };
    },
    async login(username: string, token: string): Promise<boolean> {
      try {
        await client("/api/hello", {
          headers: this.buildBasicAuthHeader(username, token),
        });

        useMessageStore().reset();
        this.token = token;
        this.username = username;
        this.authorized = true;
      } catch (error) {
        useMessageStore().setError(errorToMessage(error));
        this.token = null;
        this.username = null;
        this.authorized = false;
      }

      return this.authorized;
    },
    logout() {
      this.token = null;
      this.username = null;
      this.authorized = false;
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
