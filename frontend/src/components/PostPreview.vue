<script setup>
import Markdown from "vue3-markdown-it";
</script>
<script>
export default {
  props: {
    source: String,
  },
};
</script>
<template>
  <div>
    <Markdown class="markdown" :source="source"></Markdown>
  </div>
</template>
<style>
.markdown * {
  word-break: break-all;
  hyphens: auto;
}
</style>