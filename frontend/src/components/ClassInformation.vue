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
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{ class_name }}</h5>
      <form @submit="submit">
        <input type="text" v-model="form.korean" placeholder="시반" required />
        <input
          type="text"
          v-model="form.moderator"
          placeholder="홍길동"
          required
        />
        <input
          type="text"
          v-model="form.schedule"
          placeholder="매주 월요일 오후 5시"
          required
        />
        <input
          type="text"
          v-model="form.description"
          placeholder="이러쿵저러쿵"
          required
        />
        <button type="submit" class="btn btn-primary">변경</button>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
