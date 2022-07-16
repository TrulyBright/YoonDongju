<script setup>
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
      <h5>연락처</h5>
      <p><span class="contact-icon">📌</span>{{ address }}</p>
      <p>
        <span class="contact-icon">📧</span
        ><a :href="'mailto:' + email">{{ email }}</a>
      </p>
      <p>
        <span class="contact-icon">📞</span>회장 {{ presidentName }}
        <a :href="'tel:' + presidentTel">{{ presidentTel }}</a>
      </p>
    </div>
    <div>
      <h5>서체</h5>
      <p>
        한글/영문:
        <a href="https://fonts.google.com/specimen/Gowun+Batang?subset=korean"
          >고운 바탕</a
        >
      </p>
      <p>
        한자:
        <a
          href="https://fonts.google.com/noto/specimen/Noto+Serif+KR?subset=korean"
          >Noto Serif Korean</a
        >
      </p>
    </div>
    <div>
      <h5>정보</h5>
      <p>
        <a href="https://github.com/TrulyBright/YoonDong-ju"
          ><img
            src="@/assets/Github-Mark-32px.png"
            alt="깃허브 아이콘. 클릭하면 깃허브의 연세문학회 프로젝트 레포지토리로 이동함."
        /></a>
      </p>
    </div>
  </footer>
</template>

<style scoped>
footer {
  display: flex;
  flex-direction: column;
  background-color: white;
}
footer div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
@media (min-width: 992px) {
  /* 992px: lg */
  footer {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
  }
}
</style>
