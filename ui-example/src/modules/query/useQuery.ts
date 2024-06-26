import { ref } from "vue";
import { client, parseEventStream } from "../api/client";
import { errorToMessage } from "../api/responseError";
import { DocumentSource, QueryBody } from "./types";
import { useMessageStore } from "../messages/messageStore";
import { computeSourcesBase64 } from "../chatSession/utils";

export interface SubmitPromptResult {
  promptId: string | null;
  answer: string | null;
  error: string | null;
  sources: DocumentSource[];
}

export const useQuery = () => {
  const abortController = ref<AbortController | null>(null);
  const currentMessage = ref<string | null>(null);
  const loading = ref(false);

  const submitPrompt = async (chatSessionId: string, query: string) => {
    // Handle aborting the previous request
    if (
      abortController.value != null &&
      !abortController.value.signal.aborted
    ) {
      abortController.value.abort();
    }
    abortController.value = new AbortController();

    // Reset the current message
    currentMessage.value = null;

    // Set the loading state
    loading.value = true;

    // Create the result object
    const result: SubmitPromptResult = {
      promptId: null,
      answer: null,
      error: null,
      sources: [],
    };

    // Create the request body
    const body: QueryBody = {
      queries: [{ query }],
    };

    try {
      // Make the request
      const response = await client(`/api/query/${chatSessionId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
        signal: abortController.value.signal,
      });

      // Try to extract the prompt ID from the headers
      result.promptId = response.headers.get("X-RAGLINE-PROMPT-ID");

      // Try to extract the response source from the headers
      const sourcesBase64 = response.headers.get("X-RAGLINE-RESPONSE-SOURCE");
      result.sources = computeSourcesBase64(sourcesBase64);

      // Parse the event stream
      result.answer = "";
      currentMessage.value = "";
      for await (const chunk of parseEventStream(response)) {
        result.answer += chunk;
        currentMessage.value += chunk;
      }
    } catch (error) {
      const errorMessage = errorToMessage(error);
      result.error = errorMessage;
      useMessageStore().setError(errorMessage);
    }

    loading.value = false;

    return result;
  };

  return {
    abortController,
    currentMessage,
    loading,
    submitPrompt,
  };
};
