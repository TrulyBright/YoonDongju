<script setup>
import { useMemberStore } from "../stores/member";
</script>
<script>
export default {
  data() {
    return {
      form: {
        username: null,
        password: null,
      },
    };
  },
  methods: {
    async submit() {
      const store = useMemberStore();
      await store.requestToken(this.form);
      await store.whoAmI();
      this.$emit("close");
    },
  },
};
</script>
<template>
  <BForm @submit.prevent="submit">
    <BButton @click="$emit('close')">×</BButton>
    <h1>로그인</h1>
    <BFormInput type="text" v-model="form.username" placeholder="ID" />
    <BFormInput
      type="password"
      v-model="form.password"
      placeholder="비밀번호"
    />
    <BButton type="submit">접속</BButton>
    <div>
      <a>ID를 잊어버렸다면</a>
      <a>비밀번호를 잊어버렸다면</a>
    </div>
  </BForm>
</template>
<style></style>
