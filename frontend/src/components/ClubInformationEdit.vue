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
  <BCard>
    <h2>연락처</h2>
    <BForm @submit.prevent="submit">
      <BFormInput
        type="text"
        name="address"
        placeholder="대강당 109호"
        v-model="form.address"
      />
      <BFormInput
        type="email"
        name="email"
        placeholder="roompennoyeah@gmail.com"
        v-model="form.email"
      />
      <BFormInput
        type="text"
        name="president_name"
        placeholder="홍길동"
        v-model="form.president_name"
      />
      <BFormInput
        type="tel"
        name="president_tel"
        placeholder="010-1234-5678"
        v-model="form.president_tel"
      />
      <BFormInput
        type="url"
        name="join_form_url"
        placeholder="https://example.com"
        v-model="form.join_form_url"
      />
      <BButton type="submit">변경</BButton>
    </BForm>
  </BCard>
</template>
<style scoped></style>
