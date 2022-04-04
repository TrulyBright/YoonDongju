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
      path: "/notices",
      name: "notices",
      component: () => import("../views/PostListView.vue"),
    },
    {
      path: "/notices/:no",
      name: "notice",
      component: () => import("../views/PostView.vue"),
      props: (route) => ({ type: "notice", no: route.params.no }),
    },
    {
      path: "/write",
      name: "write",
      component: () => import("../views/PostWriteView.vue"),
    },
    {
      path: "/me",
      name: "me",
      component: () => import("../views/MeView.vue"),
    },
    {
      path: "/magazines",
      name: "magazines",
      component: () => import("../views/MagazineGridView.vue"),
    },
  ],
});

export default router;
