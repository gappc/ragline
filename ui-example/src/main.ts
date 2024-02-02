import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import { createPinia } from "pinia";
import { router } from "./routes";

const app = createApp(App);

// Add Vue router
app.use(router);

// Add pinia store
const pinia = createPinia();
app.use(pinia);

app.mount("#app");
