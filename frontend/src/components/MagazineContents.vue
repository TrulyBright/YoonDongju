<script setup>
import MagazineContent from "./MagazineContent.vue";
</script>
<script>
export default {
  props: {
    contents: Array,
  },
};
</script>
<template>
  <MagazineContent
    v-for="content in contents"
    :key="content"
    v-bind="content"
  ></MagazineContent>
</template>
<style></style>
