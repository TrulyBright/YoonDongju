<script setup>
import axios from "axios";
import PostOutlineItem from "../components/PostOutlineItem.vue";
</script>
<script>
export default {
  props: {
    skip: Number,
    limit: Number,
  },
  data() {
    return {
      items: [],
    };
  },
  created() {
    axios
      .get(
        "/notices?skip=" +
          (this.$route.query.skip || 0) +
          "&limit=" +
          (this.$route.query.limit || 20)
      )
      .then((res) => {
        this.items = res.data;
      })
      .catch((error) => {
        console.error(error);
      });
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
