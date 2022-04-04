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
    <Markdown :source="source"></Markdown>
  </div>
</template>
