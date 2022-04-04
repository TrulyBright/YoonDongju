<script setup>
import axios from "axios";
import PostOutlineItem from "../components/PostOutlineItem.vue";
</script>
<script>
export default {
  data() {
    return {
      items: [],
    };
  },
  async created() {
    try {
      const result = await axios.get(
        "/notices?skip=" +
          (this.$route.query.skip || 0) +
          "&limit=" +
          (this.$route.query.limit || 20)
      );
      this.items = result.data;
    } catch (error) {
      console.error(error);
    }
  },
};
</script>
<template>
  <main>
    <PostOutlineItem
      v-for="item in items"
      v-bind="item"
      :key="item"
    ></PostOutlineItem>
  </main>
</template>
<style scoped></style>
