<template>
  <div>
    <div>
      <h2>Query</h2>
      <input type="text" v-model="query" @keyup.enter="submit" />
      <button @click="submit">Ask</button>
    </div>
    <div>
      <h2>Full response</h2>
      <textarea class="w-full px-4 py-3 rounded" rows="7" disabled>{{
        queryResponseMessage
      }}</textarea>
      <div class="text-left opacity-50">
        <ul>
          <li v-for="{ file, pages } in sources" :key="file">
            <a :href="`/api/files/${file}`">{{ file }}</a> (page
            {{ pages.join(", ") }})
          </li>
        </ul>
      </div>
      <div class="text-sm text-gray-500">
        <span v-if="queryId">Query ID: {{ queryId }}</span>
      </div>
      <Feedback v-if="queryId" :query-id="queryId" />
    </div>
    <div v-if="queryResponseLoading">Loading...</div>
    <div v-if="queryResponseError" class="text-error">
      {{ queryResponseError }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useQuery } from "../modules/query/useQuery";
import Feedback from "./Feedback.vue";

const query = ref("");
const queryId = ref<string | null>();
const {
  queryResponseMessage,
  queryResponseError,
  queryResponseLoading,
  queryResponseSources,
  submitQuery,
} = useQuery();

const submit = async () => (queryId.value = await submitQuery(query.value));

const sources = computed(() =>
  Object.entries(queryResponseSources.value).map(([key, value]) => ({
    file: key,
    pages: value.map((v) => Number(v)).sort(),
  }))
);
</script>
