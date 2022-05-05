<script setup>
import ClassInformation from "../components/ClassInformation.vue";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      list: [],
    };
  },
  async created() {
    const response = await axios.get("classes");
    this.list = response.data;
  },
};
</script>
<template>
  <ClassInformation
    v-for="data in list"
    :key="data"
    :class_name="data.name"
  ></ClassInformation>
</template>
<style scoped></style>
