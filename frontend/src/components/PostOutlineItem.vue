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
  <div class="container">
    <div class="row text-center">
      <div class="col col-lg-auto d-none d-lg-block">{{ no }}</div>
      <RouterLink class="col" :to="{ name: 'notice', params: { no: no } }">{{
        title
      }}</RouterLink>
      <div class="col col-lg-auto d-none d-lg-block">{{ author }}</div>
      <small class="col col-lg-auto d-lg-none align-self-center">{{
        published.split("-").slice(1).join("-")
      }}</small>
      <small class="col col-lg-auto d-none d-lg-block align-self-center">{{
        published
      }}</small>
    </div>
  </div>
</template>

<style scoped>
a {
  color: var(--color-brown) !important;
}
</style>
