<script setup>
import axios from "axios";
import ClassWithRecords from "../components/ClassWithRecords.vue";
</script>
<script>
export default {
  props: {
    name: String,
  },
  data() {
    return {
      classes: [],
      shown: null,
    };
  },
  async created() {
    const response = await axios.get("classes");
    this.classes = response.data;
  },
};
</script>
<template>
  <BListGroup>
    <BListGroupItem
      v-for="c in classes"
      :key="c.name"
      :active="name === c.name"
      button
      @click="$router.push(c.name)"
      >{{ c.korean }}</BListGroupItem
    >
  </BListGroup>
  <ClassWithRecords :name="name"></ClassWithRecords>
</template>
<style scoped>
.active.list-group-item {
  background-color: pink;
  border-color: pink;
}
</style>
