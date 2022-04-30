<script setup>
import axios from "axios";
import { useMemberStore } from "../stores/member";
import MemberRow from "../components/MemberRow.vue";
</script>
<script>
const store = useMemberStore();
export default {
  data() {
    return {
      list: [],
    };
  },
  async created() {
    const response = await axios.get("members", {
      headers: {
        Authorization: store.authorizationHeader,
      },
    });
    this.list = response.data;
  },
};
</script>
<template>
  <h2>회원 관리</h2>

  <MemberRow v-for="m in list" v-bind="m" :key="m.student_id"></MemberRow>
</template>
<style scoped></style>
