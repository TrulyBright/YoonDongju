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
  <div>{{ author }}</div>
  <div>{{ language }}</div>
</template>
<style></style>
