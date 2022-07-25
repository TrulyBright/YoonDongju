<script setup>
import { RouterView } from "vue-router";
const links = {
  "/admin/club-information": "동아리",
  "/admin/members": "회원",
  "/admin/classes": "분반",
};
</script>
<template>
  <h1>관리</h1>
  <ul class="list-group">
    <li
      :class="
        'list-group-item list-group-item-action' +
        ($route.path === link ? ' active' : '')
      "
      v-for="[link, name] of Object.entries(links)"
      :key="link"
      @click="$router.push(link)"
    >
      {{ name }}
    </li>
  </ul>
  <RouterView></RouterView>
</template>
<style scoped>
.list-group-item {
  cursor: pointer;
}
</style>
