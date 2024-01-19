<template>
  <div>
    <div>
      <h2>Query</h2>
      <input type="text" v-model="queryModel" @keyup.enter="submit" />
      <button @click="submit">Ask</button>
    </div>
    <div>
      <h2>Full response</h2>
      <textarea style="width: 100%" rows="7" disabled>{{
        submitQueryMessage
      }}</textarea>
    </div>
    <div v-if="submitQueryLoading">Loading...</div>
    <div v-if="submitQueryError" style="color: red">{{ submitQueryError }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useQuery } from "../modules/query/useQuery";

const query = ref("");
const queryModel = ref("");

const { submitQueryMessage, submitQueryError, submitQueryLoading } =
  useQuery(query);

const submit = () => (query.value = queryModel.value);
</script>
