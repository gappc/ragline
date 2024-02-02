import { acceptHMRUpdate, defineStore } from "pinia";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { buildBasicAuthHeader } from "./utils";

const storageKey = "authorization";

export const useAuthStore = defineStore("authStore", () => {
  const username = ref<string | null>(null);
  const token = ref<string | null>(null);
  const authorized = ref<boolean>(false);
  const returnUrl = ref<string | null>(null);

  // Check if the authorization is stored in the session storage
  const storedAuthorization = sessionStorage.getItem(storageKey);

  // If it is, try to parse the stored authorization
  if (storedAuthorization != null) {
    try {
      const auth = JSON.parse(storedAuthorization);
      authorized.value = auth.authorized;
      username.value = auth.username;
      token.value = auth.token;
    } catch (error) {
      console.error("Failed to parse the stored authorization", error);
    }
  }

  // Computed property for the basic auth header with the current username and token
  const basicAuthHeader = computed(() =>
    buildBasicAuthHeader(username.value ?? "", token.value ?? "")
  );

  // Router instance for redirecting after login and logout
  const router = useRouter();

  // Login function. On success, it sets the authorization and redirects to the return URL
  // or the conversations page. On failure, it sets an error message and resets the authorization.
  const setCredentials = (nextUsername: string, nextToken: string) => {
    username.value = nextUsername;
    token.value = nextToken;
    authorized.value = true;

    // Store the authorization in the session storage
    sessionStorage.setItem(
      storageKey,
      JSON.stringify({
        username: username.value,
        token: token.value,
        authorized: true,
      })
    );

    router.push(returnUrl.value || { name: "home" });
  };

  // Logout function. It resets the authorization and redirects to the login page.
  const removeCredentials = () => {
    token.value = null;
    username.value = null;
    authorized.value = false;

    // Remove the authorization from the session storage
    sessionStorage.removeItem(storageKey);

    // Redirect to the login page
    router.push({ name: "login" });
  };

  // Handle changes to the session storage that are not triggered by this app
  // (e.g. changes made in developer tools)
  window.addEventListener("storage", function () {
    const storedAuthorization = sessionStorage.getItem(storageKey);
    if (storedAuthorization == null) {
      removeCredentials();
    }
  });

  return {
    username,
    token,
    authorized,
    returnUrl,
    basicAuthHeader,
    setCredentials,
    removeCredentials,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
