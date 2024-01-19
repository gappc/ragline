<template>
  <div class="flex flex-col gap-2">
    <h2 v-if="!useAuthStore().authorized" class="mb-3">Please sign in</h2>
    <div class="flex flex-col lg:flex-row gap-2 justify-center">
      <input
        type="text"
        v-model="username"
        placeholder="username"
        @keyup.enter="login"
      />
      <div class="flex gap-2">
        <input
          v-model="token"
          class="grow"
          placeholder="password"
          :type="showPassword ? 'text' : 'password'"
          @keyup.enter="login"
        />
        <button @click="showPassword = !showPassword" class="w-20">
          {{ showPassword ? "Hide" : "Show" }}
        </button>
      </div>
    </div>
    <div class="flex gap-2 justify-center">
      <button @click="login">Login</button>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "../modules/auth/authStore";
import { useFileStore } from "../modules/files/filesStore";
import { useMessageStore } from "../modules/messages/messageStore";

const token = ref("");
const username = ref("");

const showPassword = ref(false);

const login = async () => {
  useMessageStore().reset();
  const authorized = await useAuthStore().login(username.value, token.value);
  if (authorized) {
    useFileStore().fetchFiles();
  }
};
const logout = async () => {
  useAuthStore().logout();
  useMessageStore().reset();
};
</script>
