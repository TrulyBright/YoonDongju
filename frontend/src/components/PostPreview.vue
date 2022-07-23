<script setup>
import Markdown from "vue3-markdown-it";
import FileUploaded from "./FileUploaded.vue";
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
    <hr />
    <div>
      <small>첨부파일</small>
      <ul v-if="form.attached" class="list-group list-group-flush rounded">
        <li v-for="uuid in form.attached" :key="uuid" class="list-group-item">
          <FileUploaded :uuid="uuid"></FileUploaded>
        </li>
      </ul>
      <div v-else>첨부된 파일이 없습니다.</div>
    </div>
  </div>
</template>
<style>
.markdown * {
  word-break: break-all;
  hyphens: auto;
}
</style>
