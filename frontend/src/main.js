import { createApp } from "vue";
import { createPinia } from "pinia";
import axios from "axios";

import App from "./App.vue";
import router from "./router";
import BootstrapVue3 from "bootstrap-vue-3";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000/";

const app = createApp(App);

app.use(BootstrapVue3);
app.use(createPinia());
app.use(router);

app.mount("#app");
