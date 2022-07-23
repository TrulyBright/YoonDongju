<script setup>
import FileUploaded from "./FileUploaded.vue";
</script>
<script>
export default {
  props: {
    data: Array,
  },
};
</script>

<template>
  <div>
    <small>첨부파일</small>
    <ul v-if="data" class="list-group list-group-flush rounded">
      <li v-for="file in data" :key="file" class="list-group-item">
        <FileUploaded :uuid="file.uuid"></FileUploaded>
      </li>
    </ul>
    <div v-else>첨부된 파일이 없습니다.</div>
  </div>
</template>
