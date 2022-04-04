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
    },
  },
};
</script>
<template>
  <form @submit.prevent="submit">
    <button type="button" @click="$emit('close')">×</button>
    <div>
      <h1>로그인</h1>
    </div>
    <div>
      <input type="text" v-model="form.username" placeholder="ID" />
      <input type="password" v-model="form.password" placeholder="비밀번호" />
      <input type="submit" value="접속" />
    </div>
    <div>
      <a>ID를 잊어버렸다면</a>
      <a>비밀번호를 잊어버렸다면</a>
    </div>
  </form>
</template>
<style></style>
