import { client } from "../api/client";
import { errorToMessage } from "../api/responseError";
import { useMessageStore } from "../messages/messageStore";
import { useAuthStore } from "./authStore";
import { buildBasicAuthHeader } from "./utils";

// Login function. On success, it sets the authorization and redirects to the return URL
// or the conversations page. On failure, it sets an error message and resets the authorization.
export const login = async (username: string, token: string) => {
  const { setCredentials, removeCredentials } = useAuthStore();

  try {
    // Check if credentials are valid
    await client("/api/hello", {
      headers: buildBasicAuthHeader(username, token),
    });

    // Reset messages
    useMessageStore().reset();

    // Pass authorization to the auth store
    setCredentials(username, token);
  } catch (error) {
    // If the credentials are invalid, reset the authorization and set an error message
    removeCredentials();
    const errorMessage = errorToMessage(error);
    useMessageStore().setError(errorMessage);
  }
};

export const logout = () => {
  const { removeCredentials } = useAuthStore();
  removeCredentials();

  // Reset messages
  useMessageStore().reset();
};
