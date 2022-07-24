<script>
export default {
  props: {
    type: String,
    title: String,
    author: String,
    language: String,
  },
};
</script>
<template>
  <div>{{ type }}</div>
  <div>{{ title }}</div>
  <div class="text-center">{{ author }}</div>
  <div class="text-center">{{ language }}</div>
</template>
<style></style>
