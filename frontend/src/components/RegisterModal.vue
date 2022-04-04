<script setup>
import { useMemberStore } from "../stores/member";
</script>
<script>
export default {
  data() {
    return {
      form: {
        portal_id: null,
        portal_pw: null,
        real_name: null,
        username: null,
        password: null,
        passwordConfirm: null,
      },
      error: "",
    };
  },
  methods: {
    async submit() {
      if (this.validate()) {
        try {
          await useMemberStore().register(this.form);
          this.error = "";
          this.$router.push({ name: "home" });
        } catch (error) {
          console.log(error.response);
          this.error = `${error.response.status}: ${error.response.data.detail}`;
        }
      }
    },
    validate() {
      if (this.form.password === this.form.passwordConfirm) {
        this.error = "";
        return true;
      }
      this.error = "재입력된 비밀번호가 다릅니다.";
      return false;
    },
  },
};
</script>
<template>
  <form @submit.prevent="submit">
    <button type="button" @click="$emit('close')">×</button>
    <div>
      <h1>사이트 회원가입</h1>
      <p>동아리 가입은 따로 해야 합니다.</p>
      <p>사이트 비밀번호는 안전히 암호화되어 저장됩니다.</p>
      <p>
        연세포탈 비밀번호는 신촌캠 동문 인증에만 이용되며, 저장되지 않습니다.
        <small><i>연세문학회를 믿으세요.</i></small>
      </p>
    </div>
    <div>
      <input
        type="number"
        v-model="form.portal_id"
        placeholder="학번(10자리)"
        required
      />
      <input
        type="password"
        v-model="form.portal_pw"
        placeholder="연세포탈 비밀번호"
        required
      />
      <input type="text" v-model="form.real_name" placeholder="이름(실명)" />
      <input type="text" v-model="form.username" placeholder="사용할 ID" />
      <input
        type="password"
        v-model="form.password"
        placeholder="사용할 비밀번호"
        pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
        required
      />
      <input
        type="password"
        v-model="form.passwordConfirm"
        placeholder="사용할 비밀번호 재입력"
        @blur="validate"
        required
      />
      <input type="submit" value="회원가입" />
      <div>{{ error }}</div>
    </div>
  </form>
</template>
<style></style>
