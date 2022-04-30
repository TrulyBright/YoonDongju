<script setup>
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    class_name: String,
  },
  data() {
    return {
      form: {
        moderator: null,
        schedule: null,
        description: null,
        korean: null,
      },
    };
  },
  async created() {
    const response = await axios.get("classes/" + this.class_name);
    this.form.moderator = response.data.moderator;
    this.form.schedule = response.data.schedule;
    this.form.description = response.data.description;
    this.form.korean = response.data.korean;
  },
  methods: {
    async submit() {
      await axios.patch("classes/" + this.class_name, this.form, {
        headers: {
          Authorization: store.authorizationHeader,
        },
      });
      this.$router.go();
    },
  },
};
</script>
<template>
  <BCard>
    <h3>{{ class_name }}</h3>
    <BForm @submit="submit">
      <BFormInput
        type="text"
        v-model="form.korean"
        placeholder="시반"
        required
      ></BFormInput>
      <BFormInput
        type="text"
        v-model="form.moderator"
        placeholder="홍길동"
        required
      ></BFormInput>
      <BFormInput
        type="text"
        v-model="form.schedule"
        placeholder="매주 월요일 오후 5시"
        required
      ></BFormInput>
      <BFormTextarea
        type="text"
        v-model="form.description"
        placeholder="이러쿵저러쿵"
        required
      ></BFormTextarea>
      <BButton type="submit">변경</BButton>
    </BForm>
  </BCard>
</template>
<style scoped></style>
