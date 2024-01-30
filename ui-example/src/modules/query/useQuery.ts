import { ref } from "vue";
import { client, parseEventStream } from "../api/client";
import { errorToMessage } from "../api/responseError";
import { QueryBody } from "./types";
import { useMessageStore } from "../messages/messageStore";

const abortController = ref<AbortController | null>(null);

export const useQuery = () => {
  const queryResponseMessage = ref("");
  const queryResponseError = ref("");
  const queryResponseLoading = ref(false);
  const queryResponseSources = ref<Record<string, string[]>>({});

  const submitQuery = async (query: string) => {
    queryResponseMessage.value = "";
    queryResponseError.value = "";
    queryResponseLoading.value = true;
    queryResponseSources.value = {};

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

      // Try to extract the response source from the headers
      const responseSourceBase64 = response.headers.get(
        "X-RAGLINE-RESPONSE-SOURCE"
      );
      if (responseSourceBase64 != null) {
        const responseSource = atob(responseSourceBase64);
        queryResponseSources.value = JSON.parse(responseSource);
      }

      // Parse the event stream
      for await (const chunk of parseEventStream(response)) {
        queryResponseMessage.value += chunk;
      }

      return response.headers.get("X-RAGLINE-QUERY-ID");
    } catch (error) {
      useMessageStore().setError(errorToMessage(error));
    } finally {
      queryResponseLoading.value = false;
    }
  };

  return {
    queryResponseMessage,
    queryResponseError,
    queryResponseLoading,
    queryResponseSources,
    submitQuery,
  };
};
