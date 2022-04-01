import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/PostView.vue"),
      props: { type: "about" },
    },
    {
      path: "/rules",
      name: "rules",
      component: () => import("../views/PostView.vue"),
      props: { type: "rules" },
    },
    {
      path: "/notices/:no",
      name: "notice",
      component: () => import("../views/PostView.vue"),
      props: (route) => ({ type: "notice", no: route.params.no }),
    },
  ],
});

export default router;
