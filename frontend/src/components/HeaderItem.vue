<script setup>
import { RouterLink } from "vue-router";
import LoginModal from "@/components/LoginModal.vue";
import { useMemberStore } from "../stores/member";
</script>
<script>
export default {
  data() {
    return {
      openLoginModal: false,
      store: useMemberStore(),
    };
  },
};
</script>
<template>
  <header>
    <RouterLink to="/">연세문학회</RouterLink>
    <RouterLink to="/about">소개</RouterLink>
    <RouterLink to="/classes">분반</RouterLink>
    <RouterLink to="/magazines">문집</RouterLink>
    <RouterLink to="/notices">공지</RouterLink>
    <RouterLink to="/admin" v-if="store.isAdmin">관리</RouterLink>
    <RouterLink to="/me" v-if="store.isAuthenticated">내정보</RouterLink>
    <a @click="openLoginModal = true" v-if="!store.isAuthenticated">로그인</a>
    <Teleport to="#app">
      <LoginModal
        v-if="openLoginModal"
        @close="openLoginModal = false"
      ></LoginModal>
    </Teleport>
    <a @click="store.logOut()" v-if="store.isAuthenticated">로그아웃</a>
  </header>
</template>

<style scoped>
header {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
</style>
