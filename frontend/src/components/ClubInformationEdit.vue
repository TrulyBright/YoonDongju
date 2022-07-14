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
        <input
          type="text"
          class="form-control"
          v-model="form.address"
          placeholder="대강당 109호"
        />
        <input
          type="email"
          class="form-control"
          v-model="form.email"
          placeholder="roompennoyeah@gmail.com"
        />
        <input
          type="text"
          class="form-control"
          v-model="form.president_name"
          placeholder="홍길동"
        />
        <input type="tel" class="form-control" v-model="form.president_tel" placeholder="010-1234-5678"/>
        <input
          type="url"
          class="form-control"
          v-model="form.join_form_url"
          placeholder="http://example.com"
        />
        <button type="submit" class="btn btn-primary">게시</button>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
