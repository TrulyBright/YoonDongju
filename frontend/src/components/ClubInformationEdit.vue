<script setup>
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
        join_form_url: null,
      },
    };
  },
  async created() {
    const response = await axios.get("club-information");
    Object.entries(response.data).forEach(([key, value]) => {
      this.form[key] = value;
    });
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
            type="url"
            class="form-control"
            id="join-form-url"
            v-model="form.join_form_url"
            placeholder="http://example.com"
          />
          <label for="join-form-url">동아리 회원가입 주소</label>
        </div>

        <button type="submit" class="btn btn-primary">게시</button>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
