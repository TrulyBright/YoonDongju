<script setup>
import { Tooltip } from "bootstrap";
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  data() {
    return {
      form: {
        address: null,
        email: null,
        president_name: null,
        president_tel: null,
        HR_chief_tel: null,
      },
    };
  },
  async created() {
    const response = await axios.get("club-information");
    Object.entries(response.data).forEach(([key, value]) => {
      this.form[key] = value;
    });
    const tooltipTriggerList = document.querySelectorAll(
      '[data-bs-toggle="tooltip"]'
    );
    [...tooltipTriggerList].map(
      (tooltipTriggerEl) => new Tooltip(tooltipTriggerEl)
    );
  },
  methods: {
    async submit() {
      await axios.put("club-information", this.form, {
        headers: {
          Authorization: store.authorizationHeader,
        },
      });
      this.$router.go(); // refresh
    },
  },
};
</script>
<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">연락처</h5>
      <form @submit.prevent="submit">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="address"
            v-model="form.address"
            placeholder="대강당 109호"
          />
          <label for="address">주소</label>
        </div>
        <div class="form-floating">
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="form.email"
            placeholder="roompennoyeah@gmail.com"
          />
          <label for="email">메일주소</label>
        </div>
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="president-name"
            v-model="form.president_name"
            placeholder="홍길동"
          />
          <label for="president-name">회장 실명</label>
        </div>
        <div class="form-floating">
          <input
            type="tel"
            class="form-control"
            id="president-tel"
            v-model="form.president_tel"
            placeholder="010-1234-5678"
          />
          <label for="president-tel">회장 전화번호</label>
        </div>
        <div class="form-floating">
          <input
            type="tel"
            class="form-control"
            id="Hr-chief-tel"
            v-model="form.HR_chief_tel"
            placeholder="010-0000-0000"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            title="이 번호로 신규 회원 가입 알림이 전송됩니다. 대시('-') 없이 숫자만 넣으세요."
          />
          <label for="HR-chief-tel">인사행정팀장 전화번호</label>
        </div>
        <button type="submit" class="btn btn-primary">게시</button>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
