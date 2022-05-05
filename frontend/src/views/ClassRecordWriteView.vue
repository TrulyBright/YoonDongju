<script setup>
import ClassRecordWrite from "../components/ClassRecordWrite.vue";
</script>
<script>
export default {
  props: {
    name: String,
  },
};
</script>
<template>
  <ClassRecordWrite
    :name="name"
    :conducted="$route.query.conducted"
  ></ClassRecordWrite>
</template>
<style scoped></style>
