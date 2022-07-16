<script setup>
import Markdown from "vue3-markdown-it";
</script>
<script>
export default {
  props: {
    form: Object,
  },
};
</script>
<template>
  <div>
    <h1>{{ form.title }}</h1>
    <Markdown class="markdown" :source="form.content"></Markdown>
    <div>{{ form.attached }}</div>
  </div>
</template>
<style>
.markdown * {
  word-break: break-all;
  hyphens: auto;
}
</style>
