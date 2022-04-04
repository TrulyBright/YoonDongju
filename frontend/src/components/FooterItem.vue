<script setup>
import { RouterLink } from "vue-router";
import RegisterModal from "@/components/RegisterModal.vue";
import { useMemberStore } from "../stores/member";
</script>
<script>
export default {
  data() {
    return {
      openRegisterModal: false,
      store: useMemberStore(),
    };
  },
  props: {
    address: String,
    email: String,
    presidentName: String,
    presidentTel: String,
    joinFormUrl: String,
  },
  computed: {
    getTheYear() {
      return new Date().getFullYear();
    },
  },
};
</script>
<template>
  <footer>
    <div>
      <p>연락처</p>
      <div>📌 {{ address }}</div>
      <div>
        📧 <a :href="'mailto:' + email">{{ email }}</a>
      </div>
      <div>
        📞 회장 {{ presidentName }}
        <a :href="'tel:' + presidentTel">{{ presidentTel }}</a>
      </div>
    </div>
    <div>
      <p>가입</p>
      <div><a :href="joinFormUrl">동아리 회원가입</a></div>
      <div>
        <a @click="openRegisterModal = true" v-if="!store.isAuthenticated"
          >사이트 회원가입</a
        >
      </div>
      <Teleport to="#app">
        <RegisterModal
          v-if="openRegisterModal"
          @close="openRegisterModal = false"
        ></RegisterModal>
      </Teleport>
    </div>
    <div>
      <p>정보</p>
      <RouterLink to="/rules">동아리 회칙</RouterLink>
      <div>
        <a :href="'https://github.com/TrulyBright/YoonDong-ju'">Github</a>
      </div>
      <div>서체: 고운 바탕(한글/영문) / Noto Serif KR (한자)</div>
      <div>
        © {{ getTheYear }} 연세문학회 | 작품 저작권은 항상 작가에게 있습니다.
      </div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}
footer div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
