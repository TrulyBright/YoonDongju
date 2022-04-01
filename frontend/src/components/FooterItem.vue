<script setup>
import { RouterLink } from "vue-router";
</script>
<script>
export default {
  props: {
    address: String,
    email: String,
    presidentName: String,
    presidentTel: String,
    joinFormUrl: String,
  },
  methods: {
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
      <div>{{ address }}</div>
      <div><a :href="'mailto:' + email"></a></div>
      <div>회장 {{ presidentName }} <a :href="'tel:' + presidentTel"></a></div>
    </div>
    <div>
      <p>가입</p>
      <div><a :href="joinFormUrl">동아리 회원가입</a></div>
      <RouterLink to="/register">사이트 회원가입</RouterLink>
    </div>
    <div>
      <p>정보</p>
      <RouterLink to="/rules">동아리 회칙</RouterLink>
      <div>
        <a :href="'https://github.com/TrulyBright/YoonDong-ju'">Github</a>
      </div>
      <div>서체: 고운 바탕(한글/영문) / Noto Serif KR (한자)</div>
      <div>
        © {{ getTheYear() }} 연세문학회 | 작품 저작권은 항상 작가에게 있습니다.
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
