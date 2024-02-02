<template>
  <AppLayout>
    <div class="flex justify-between items-center bg-black px-2">
      <div></div>
      <ul class="flex bg-black gap-2 mt-2">
        <li
          class="flex items-center rounded-b-none py-2 px-4"
          :class="[{ 'bg-black': name !== 'conversations' }]"
        >
          <router-link :to="{ name: 'conversations' }" class="bg-inherit">
            Your questions
          </router-link>
        </li>
        <li
          class="flex items-center rounded-b-none py-2 px-4"
          :class="[{ 'bg-black': name !== 'documents' }]"
        >
          <router-link :to="{ name: 'documents' }" class="bg-inherit">
            Document library
          </router-link>
        </li>
      </ul>
      <ButtonCustom size="sm" @click="logout" variant="ghost">
        Logout
      </ButtonCustom>
    </div>
    <div class="flex flex-1 px-2 overflow-y-auto">
      <slot></slot>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import ButtonCustom from "../components/button/ButtonCustom.vue";
import { logout } from "../modules/auth/auth";
import AppLayout from "./AppLayout.vue";

const { name } = useRoute();
</script>
