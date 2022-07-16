<script setup>
import axios from "axios";
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
    <ul v-if="data" class="list-group list-group-flush">
      <li v-for="file in data" :key="file" class="list-group-item">
        <a :href="axios.defaults.baseURL + 'uploaded/' + file.uuid">
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
          ></a
        >
      </li>
    </ul>
    <div v-else>첨부된 파일이 없습니다.</div>
  </div>
</template>
