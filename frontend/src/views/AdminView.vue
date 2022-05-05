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
  <BListGroup>
    <BListGroupItem
      v-for="[link, name] of Object.entries(links)"
      :key="link"
      :active="$route.path === link"
      button
      @click="$router.push(link)"
    >
      {{ name }}
    </BListGroupItem>
  </BListGroup>
  <RouterView></RouterView>
</template>
<style scoped></style>
