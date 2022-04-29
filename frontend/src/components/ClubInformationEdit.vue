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
  <form @submit.prevent="submit">
    <label for="address"
      >위치
      <input
        type="text"
        name="address"
        placeholder="대강당 109호"
        :value="form.address"
        @input="(event) => (form.address = event.target.value)"
      />
    </label>
    <label for="email"
      >이메일
      <input
        type="email"
        name="email"
        placeholder="roompennoyeah@gmail.com"
        :value="form.email"
        @input="(event) => (form.email = event.target.value)"
      />
    </label>
    <label for="president_name"
      >회장
      <input
        type="text"
        name="president_name"
        placeholder="홍길동"
        :value="form.president_name"
        @input="(event) => (form.president_name = event.target.value)"
      />
    </label>
    <label for="president_tel"
      >전화번호
      <input
        type="tel"
        name="president_tel"
        placeholder="010-1234-5678"
        :value="form.president_tel"
        @input="(event) => (form.president_tel = event.target.value)"
      />
    </label>
    <label for="join_form_url"
      >가입 구글 폼 주소
      <input
        type="url"
        name="join_form_url"
        placeholder="https://example.com"
        :value="form.join_form_url"
        @input="(event) => (form.join_form_url = event.target.value)"
      />
    </label>
    <input type="submit" value="변경" />
  </form>
</template>
<style scoped></style>
