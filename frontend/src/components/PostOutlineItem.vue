<script setup>
import { RouterLink } from "vue-router";
</script>
<script>
export default {
  props: {
    no: Number,
    title: String,
    author: String,
    published: String,
  },
};
</script>

<template>
  <div class="item">
    <div>{{ no }}</div>
    <RouterLink :to="{ name: 'notice', params: { no: no } }">{{
      title
    }}</RouterLink>
    <div>{{ author }}</div>
    <div>{{ published }}</div>
  </div>
</template>

<style scoped>
.item {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
}
</style>
