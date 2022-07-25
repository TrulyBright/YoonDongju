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
      <form @submit.prevent="submit">
        <div class="form-floating">
          <input
            class="form-control"
            id="class-title"
            type="text"
            v-model="form.korean"
            placeholder="시반"
            required
          />
          <label for="class-title">분반명</label>
        </div>
        <div class="form-floating">
          <input
            class="form-control"
            type="text"
            v-model="form.moderator"
            placeholder="홍길동"
            id="class-moderator"
            required
          />
          <label for="class-moderator">분반장</label>
        </div>
        <div class="form-floating">
          <input
            class="form-control"
            type="text"
            v-model="form.schedule"
            placeholder="매주 월요일 오후 5시"
            id="class-schedule"
            required
          />
          <label for="class-schedule">운영일정</label>
        </div>
        <div class="form-floating mb-1">
          <input
            class="form-control"
            type="text"
            v-model="form.description"
            placeholder="이러쿵저러쿵"
            required
            id="class-description"
          />
          <label for="class-description">설명</label>
        </div>
        <button type="submit" class="btn btn-primary">변경</button>
      </form>
    </div>
  </div>
</template>
<style scoped></style>
