import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import { Amplify } from "aws-amplify";
import awsconfig from "../aws-exports";

Amplify.configure(awsconfig);

const app = createApp(App);
const pinia = createPinia(); // dependency for storing global states

app.use(pinia);
app.use(router);
app.mount("#app");
