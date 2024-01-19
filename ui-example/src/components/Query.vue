<template>
  <div>
    Query:
    <input type="text" v-model="query" @keyup.enter="submit" />
    <button @click="submit">Ask</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const query = ref("");

const emit = defineEmits(["submit"]);

const submit = () => emit("submit", query.value);
</script>
