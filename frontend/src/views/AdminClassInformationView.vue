<script setup>
import ClassInformation from "../components/ClassInformation.vue";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      names: [],
    };
  },
  async created() {
    const response = await axios.get("classes");
    this.names = response.data;
  },
};
</script>
<template>
  <h2>분반 소개</h2>
  <ClassInformation
    v-for="name in names"
    :key="name"
    :class_name="name"
  ></ClassInformation>
</template>
<style scoped></style>
