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
    <div class="row text-center d-none d-lg-grid">
      <div class="post-no align-self-center">{{ no }}</div>
      <RouterLink
        class="post-title"
        :to="{ name: 'notice', params: { no: no } }"
        >{{ title }}</RouterLink
      >
      <div class="post-author align-self-center">{{ author }}</div>
      <small class="post-published align-self-center">{{ published }}</small>
    </div>
    <div class="d-lg-none">
      <RouterLink :to="{ name: 'notice', params: { no: no } }">{{
        title
      }}</RouterLink>
      <small class="align-self-center">{{
        published.split("-").slice(1).join("-")
      }}</small>
    </div>
  </div>
</template>
<style scoped lang="scss">
a {
  color: var(--color-brown) !important;
}
.row {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
}
div.d-lg-none {
  display: grid;
  grid-template-columns: 1fr auto;
}
</style>
