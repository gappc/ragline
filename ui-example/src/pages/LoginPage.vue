<template>
  <AppLayout class="flex items-center justify-center">
    <form
      class="flex flex-col gap-4 w-full md:w-[30rem] px-2"
      @submit.prevent="loginInternal"
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
          <button @click="showPassword = !showPassword" type="button">
            <IconVisibilityOff />
          </button>
        </template>
      </InputCustom>
      <ButtonCustom @click="loginInternal">Login</ButtonCustom>
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
import { login, logout } from "../modules/auth/auth";
import { useMessageStore } from "../modules/messages/messageStore";

const username = ref("");
const token = ref("");
const showPassword = ref(false);

const { message } = storeToRefs(useMessageStore());

const loginInternal = async () => await login(username.value, token.value);

onBeforeMount(() => logout());
</script>
