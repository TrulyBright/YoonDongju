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
  <PostWrite :type="type" :no="$route.query.no"></PostWrite>
</template>
<style></style>
