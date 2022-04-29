<script setup>
import { RouterView } from "vue-router";
</script>
<script>
export default {};
</script>
<template>
  <h1>관리</h1>
  <div>
    <RouterLink to="/admin/club-information">동아리 정보</RouterLink>
    <RouterLink to="/admin/members">회원 관리</RouterLink>
    <RouterLink to="/admin/classes">분반 정보</RouterLink>
  </div>
  <RouterView></RouterView>
</template>
<style scoped></style>
