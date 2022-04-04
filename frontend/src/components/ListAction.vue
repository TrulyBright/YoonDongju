<script setup>
import { RouterLink } from "vue-router";
</script>
<script>
export default {
  props: {
    routeName: String,
  },
  computed: {
    writingLink() {
      return this.routeName === "class" ? "classWrite" : "write";
    },
  },
};
</script>
<template>
  <RouterLink :to="writingLink">글쓰기</RouterLink>
</template>
<style></style>
