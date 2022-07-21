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
  <div class="item d-flex justify-content-between">
    <div class="d-none d-lg-block">{{ no }}</div>
    <RouterLink :to="{ name: 'notice', params: { no: no } }">{{
      title
    }}</RouterLink>
    <div class="d-none d-lg-block">{{ author }}</div>
    <small class="published d-lg-none align-self-center">{{ published.split("-").slice(1,).join("-") }}</small>
    <small class="published d-none d-lg-block align-self-center">{{ published }}</small>
  </div>
</template>

<style scoped>
a {
  color: var(--color-brown) !important;
}
</style>
