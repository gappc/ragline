import { ref } from "vue";
import { QueryBody } from "./types";

const abortController = ref<AbortController | null>(null);

export const useQuery = () => {
  const submitQueryMessage = ref("");
  const submitQueryError = ref("");
  const submitQueryLoading = ref(false);

  const submitQuery = async (query: string) => {
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
      queries: [{ query }],
    };

    try {
      const response = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: abortController.value.signal,
      });

      if (response.status >= 400) {
        console.log("Error:", response);
        const message = {
          status: response.status,
          statusText: response.statusText,
          body: await response.text(),
        };
        throw new Error(JSON.stringify(message));
      }

      const reader = response.body?.getReader();
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
    } catch (error) {
      submitQueryError.value =
        error instanceof Error ? error.message : JSON.stringify(error);
    } finally {
      submitQueryLoading.value = false;
    }
  };

  return {
    submitQueryMessage,
    submitQueryError,
    submitQueryLoading,
    submitQuery,
  };
};
