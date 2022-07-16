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
    <hr />
    <div>
      <small>첨부파일</small>
      <ul v-if="form.attachedScheduled" class="list-group list-group-flush">
        <li
          v-for="file in form.attachedScheduled"
          :key="file"
          class="list-group-item"
        >
          <small
            ><i
              :class="
                'bi-filetype-' +
                file.name
                  .split('.')
                  [file.name.split('.').length - 1].toLowerCase()
              "
            ></i
            >{{ file.name }}</small
          >
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
