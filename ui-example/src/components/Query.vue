<template>
  <div>
    <div>
      <h2>Query</h2>
      <input type="text" v-model="queryModel" @keyup.enter="submit" />
      <button @click="submit">Ask</button>
    </div>
    <div>
      <h2>Full response</h2>
      <textarea class="w-full px-4 py-3 rounded" rows="7" disabled>{{
        submitQueryMessage
      }}</textarea>
    </div>
    <div v-if="submitQueryLoading">Loading...</div>
    <div v-if="submitQueryError" class="text-error">{{ submitQueryError }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useQuery } from "../modules/query/useQuery";

const query = ref("");
const queryModel = ref("");

const {
  submitQueryMessage,
  submitQueryError,
  submitQueryLoading,
  submitQuery,
} = useQuery();

const submit = () => submitQuery(query.value);
</script>
