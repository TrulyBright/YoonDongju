<script setup>
import { RouterLink } from "vue-router";
</script>
<template>
  <header>
    <RouterLink to="/">연세문학회</RouterLink>
    <RouterLink to="/about">소개</RouterLink>
    <RouterLink to="/classes">분반</RouterLink>
    <RouterLink to="/magazines">문집</RouterLink>
    <RouterLink to="/notices">공지</RouterLink>
    <RouterLink to="/admin">관리</RouterLink>
    <RouterLink to="/me">내정보</RouterLink>
  </header>
</template>

<style scoped>
header {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
</style>
