<script setup>
import ClassRecordItem from "../components/ClassRecordItem.vue";
</script>
<script>
export default {
  props: {
    name: String,
    conducted: String,
  },
};
</script>
<template>
  <ClassRecordItem :name="name" :conducted="conducted"></ClassRecordItem>
</template>
<style scoped></style>
