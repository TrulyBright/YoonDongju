<script>
export default {
  props: {
    username: String,
    real_name: String,
    student_id: Number,
    role: String,
  },
  computed: {
    roleInKorean() {
      switch (this.role) {
        case "member":
          return "회원";
        case "board":
          return "임원";
        case "president":
          return "회장";
        default:
          return "불명";
      }
    },
  },
};
</script>
<template>
  <div>{{ username }}</div>
  <div>{{ real_name }}</div>
  <div>{{ student_id }}</div>
  <div>{{ roleInKorean }}</div>
  <div>
    <button type="button">권한 변경</button>
  </div>
</template>
<style scoped></style>
