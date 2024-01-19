<template>
  <div style="display: flex; flex-direction: column; gap: 30px">
    <Upload />
    <Query @submit="submit" />
    <Response :response="response" style="text-align: left" />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Upload from "./components/Upload.vue";
import Query from "./components/Query.vue";
import Response from "./components/Response.vue";

interface Query {
  query: string;
  filter?: unknown[];
  top_k?: number[];
}

interface QueryBody {
  queries: Query[];
}

const response = ref("");
const abortController = ref<AbortController | null>(null);

const submit = async (query: string) => {
  if (abortController.value != null && !abortController.value.signal.aborted) {
    abortController.value.abort();
  }
  abortController.value = new AbortController();

  response.value = "";

  const body: QueryBody = {
    queries: [{ query }],
  };

  const fetchResult = await fetch("/api/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: abortController.value.signal,
  });
  const reader = fetchResult.body?.getReader();
  const decoder = new TextDecoder("utf-8");
  while (true) {
    const { value, done } = await reader!.read();
    if (done) break;
    const decodedValue = decoder.decode(value);
    console.log("Received", decodedValue);
    response.value += decodedValue;
  }
};
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
