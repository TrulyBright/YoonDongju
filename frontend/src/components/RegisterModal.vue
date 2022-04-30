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
          this.$emit("close");
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
  <BForm @submit.prevent="submit">
    <BButton @click="$emit('close')">×</BButton>
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
      <BFormInput
        type="number"
        v-model="form.portal_id"
        placeholder="학번(10자리)"
        required
      />
      <BFormInput
        type="password"
        v-model="form.portal_pw"
        placeholder="연세포탈 비밀번호"
        required
      />
      <BFormInput
        type="text"
        v-model="form.real_name"
        placeholder="실명"
        required
      />
      <BFormGroup
        description="ID는 최대 64자에, 한글을 비롯하여 어떤 문자든 허용됩니다."
      >
        <BFormInput
          type="text"
          v-model="form.username"
          placeholder="사용할 ID"
          pattern="^.{1,65}$"
          required
      /></BFormGroup>
      <BFormGroup
        description="비밀번호는 10자 이상에 숫자와 영문이 하나씩은 있어야 합니다."
        ><BFormInput
          type="password"
          v-model="form.password"
          placeholder="사용할 비밀번호"
          pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
          required
      /></BFormGroup>
      <BFormInput
        type="password"
        v-model="form.passwordConfirm"
        placeholder="사용할 비밀번호 재입력"
        @blur="validate"
        required
      />
      <BButton type="submit">가입</BButton>
      <div>{{ error }}</div>
    </div>
  </BForm>
</template>
<style></style>
