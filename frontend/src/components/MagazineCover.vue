<script setup>
import axios from "axios";
</script>
<script>
export default {
  props: {
    cover: String,
    published: String,
  },
};
</script>
<template>
  <img
    :src="axios.defaults.baseURL + 'uploaded/' + cover"
    :alt="published + '에 발행된 문집 표지'"
  />
</template>
<style scoped>
img {
  max-width: 100%;
  max-height: 100%;
}
</style>
