<template>
  <AppLayout class="flex items-center justify-center">
    <form
      class="flex flex-col gap-4 w-full md:w-[30rem] px-2"
      @submit.prevent="login"
    >
      <InputCustom
        v-model="username"
        autocomplete="username"
        placeholder="Username"
        autofocus
      >
        <template #prepend><IconAccountCircle /></template>
      </InputCustom>
      <InputCustom
        v-model="token"
        autocomplete="current-password"
        placeholder="Password"
        :type="showPassword ? 'text' : 'password'"
      >
        <template #prepend><IconLock /></template>
        <template #append>
          <button @click="showPassword = !showPassword">
            <IconVisibilityOff />
          </button>
        </template>
      </InputCustom>
      <ButtonCustom @click="login">Login</ButtonCustom>
    </form>
    <div class="mt-2">{{ message ? message : "&nbsp;" }}</div>
  </AppLayout>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { onBeforeMount, ref } from "vue";
import ButtonCustom from "../components/button/ButtonCustom.vue";
import InputCustom from "../components/input/InputCustom.vue";
import IconAccountCircle from "../components/svg/IconAccountCircle.vue";
import IconLock from "../components/svg/IconLock.vue";
import IconVisibilityOff from "../components/svg/IconVisibilityOff.vue";
import AppLayout from "../layouts/AppLayout.vue";
import { useAuthStore } from "../modules/auth/authStore";
import { useMessageStore } from "../modules/messages/messageStore";

const username = ref("");
const token = ref("");
const showPassword = ref(false);

const { message } = storeToRefs(useMessageStore());

const login = async () =>
  await useAuthStore().login(username.value, token.value);

onBeforeMount(() => useAuthStore().logout());
</script>
