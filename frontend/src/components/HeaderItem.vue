<script setup>
import LoginModal from "@/components/LoginModal.vue";
import { useMemberStore } from "../stores/member";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      openLoginModal: false,
      store: useMemberStore(),
      classes: [],
    };
  },
  async created() {
    const response = await axios.get("classes");
    this.classes = response.data;
  },
};
</script>
<template>
  <header>
    <BButton to="/">연세문학회</BButton>
    <BButton to="/about">소개</BButton>
    <BDropdown text="분반">
      <BDropdownItem v-for="c in classes" :key="c" :to="'/classes/' + c.name">{{
        c.korean
      }}</BDropdownItem>
    </BDropdown>
    <BButton to="/magazines">문집</BButton>
    <BButton to="/notices">공지</BButton>
    <BButton to="/admin" v-if="store.isAdmin">관리</BButton>
    <BButton to="/me" v-if="store.isAuthenticated">내정보</BButton>
    <BButton @click="openLoginModal = true" v-if="!store.isAuthenticated"
      >로그인</BButton
    >
    <Teleport to="#app">
      <LoginModal
        v-if="openLoginModal"
        @close="openLoginModal = false"
      ></LoginModal>
    </Teleport>
    <BButton to="/" @click="store.logOut" v-if="store.isAuthenticated"
      >로그아웃</BButton
    >
  </header>
</template>

<style>
header {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
</style>
