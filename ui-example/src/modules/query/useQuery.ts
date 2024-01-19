import { MaybeRef, ref, toValue, watch } from "vue";
import { QueryBody } from "./types";

const abortController = ref<AbortController | null>(null);

export const useQuery = (query: MaybeRef<string>) => {
  const submitQueryMessage = ref("");
  const submitQueryError = ref("");
  const submitQueryLoading = ref(false);

  watch(
    () => toValue(query),
    async (queryValue) => {
      submitQueryMessage.value = "";
      submitQueryError.value = "";
      submitQueryLoading.value = true;

      if (
        abortController.value != null &&
        !abortController.value.signal.aborted
      ) {
        abortController.value.abort();
      }
      abortController.value = new AbortController();

      const body: QueryBody = {
        queries: [{ query: queryValue }],
      };

      fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: abortController.value.signal,
      })
        .then((response) => response.body?.getReader())
        .then(async (reader) => {
          const decoder = new TextDecoder("utf-8");
          while (true) {
            const { value, done } = await reader!.read();
            if (done) {
              break;
            }
            const decodedValue = decoder.decode(value);
            console.log("Received", decodedValue);
            submitQueryMessage.value += decodedValue;
          }
        })
        .catch((error) => {
          submitQueryError.value =
            error instanceof Error ? error.message : JSON.stringify(error);
        })
        .finally(() => {
          submitQueryLoading.value = false;
        });
    }
  );

  return { submitQueryMessage, submitQueryError, submitQueryLoading };
};
