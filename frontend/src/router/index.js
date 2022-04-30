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
      props: { type: "notices" },
    },
    {
      path: "/notices/:no",
      name: "notice",
      component: () => import("../views/PostView.vue"),
      props: (route) => ({ type: "notices", no: Number(route.params.no) }),
    },
    {
      path: "/notices/write",
      name: "writeNotice",
      component: () => import("../views/PostWriteView.vue"),
      props: { type: "notices" },
    },
    {
      path: "/about/write",
      name: "writeAbout",
      component: () => import("../views/PostWriteView.vue"),
      props: { type: "about" },
    },
    {
      path: "/rules/write",
      name: "writeRules",
      component: () => import("../views/PostWriteView.vue"),
      props: { type: "rules" },
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
    {
      path: "/magazines/write",
      name: "magazineWrite",
      component: () => import("../views/MagazineWriteView.vue"),
    },
    {
      path: "/classes",
      name: "classes",
      component: () => import("../views/ClassesView.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("../views/AdminView.vue"),
      children: [
        {
          path: "club-information",
          component: () => import("../views/AdminClubInformationView.vue"),
        },
        {
          path: "classes",
          component: () => import("../views/AdminClassInformationView.vue"),
        },
        {
          path: "members",
          component: () => import("../views/AdminMemberList.vue"),
        },
      ],
    },
  ],
});

export default router;
