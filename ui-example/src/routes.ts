import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "./modules/auth/authStore";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      redirect: "/conversations",
    },
    {
      path: "/conversations",
      name: "conversations",
      component: () => import("./pages/ConversationsPage.vue"),
    },
    {
      path: "/documents",
      name: "documents",
      component: () => import("./pages/DocumentsPage.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("./pages/LoginPage.vue"),
    },
  ],
});

router.beforeEach(async (to) => {
  // Redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (authRequired && !auth.authorized) {
    // Store the return URL for redirecting after login
    auth.returnUrl = to.fullPath;
    return { name: "login" };
  }
});
