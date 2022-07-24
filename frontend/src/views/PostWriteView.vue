<script setup>
import PostWrite from "@/components/PostWrite.vue";
</script>
<script>
export default {
  props: {
    type: String,
  },
};
</script>
<template>
  <PostWrite :type="type" :no="Number($route.query.no)"></PostWrite>
</template>
<style></style>
