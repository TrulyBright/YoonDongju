<script>
export default {
  props: {
    username: String,
    studentId: Number,
    realName: String,
    role: String,
  },
};
</script>
<template>
  <div>
    <div>ID: {{ username }}</div>
    <div>학번: {{ studentId }}</div>
    <div>실명: {{ realName }}</div>
    <div>직위: {{ role }}</div>
  </div>
</template>
<style></style>
