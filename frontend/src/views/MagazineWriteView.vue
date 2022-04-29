<script setup>
import MagazineWriter from "../components/MagazineWriter.vue";
</script>
<script>
export default {
  props: {},
  data() {
    return {};
  },
};
</script>
<template>
  <MagazineWriter :published="$route.query.published"></MagazineWriter>
</template>
<style scoped></style>
