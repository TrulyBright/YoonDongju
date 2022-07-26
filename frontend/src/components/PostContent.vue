<script setup>
import Markdown from "vue3-markdown-it";
</script>
<script>
export default {
  props: {
    content: String,
  },
};
</script>

<template>
  <div><Markdown :source="content" class="markdown"></Markdown></div>
</template>
<style>
.markdown * {
  word-break: break-all;
  hyphens: auto;
}
.markdown img {
  max-width: 100%;
  height: auto;
}
</style>
