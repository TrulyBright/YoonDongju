<script setup>
import MagazineItem from "../components/MagazineItem.vue";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      magazines: [],
    };
  },
  async created() {
    const response = await axios.get("magazines");
    this.magazines = response.data;
  },
};
</script>
<template>
  <div>
    <MagazineItem
      v-for="volume in magazines"
      :key="volume.published"
      v-bind="volume"
    ></MagazineItem>
  </div>
</template>
<style></style>
