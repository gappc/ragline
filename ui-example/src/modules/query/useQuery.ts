import { ref } from "vue";
import { client, parseEventStream } from "../api/client";
import { errorToMessage } from "../api/responseError";
import { QueryBody } from "./types";
import { useMessageStore } from "../messages/messageStore";

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
      const response = await client("/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
        signal: abortController.value.signal,
      });

      for await (const chunk of parseEventStream(response)) {
        submitQueryMessage.value += chunk;
      }

      return response.headers.get("X-RAGLINE-QUERY-ID");
    } catch (error) {
      useMessageStore().setError(errorToMessage(error));
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
