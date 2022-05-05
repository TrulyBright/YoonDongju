<script setup>
import axios from "axios";
</script>
<script>
export default {
  props: {
    uuid: String,
  },
  data() {
    return {
      file: {
        uuid: "",
        name: "",
        contentType: "",
      },
    };
  },
  async created() {
    const response = await axios.get("uploaded-info/" + this.uuid);
    this.file.uuid = response.data.uuid;
    this.file.name = response.data.name;
    this.file.contentType = response.data.content_type;
  },
};
</script>
<template>
  <div>
    <a :href="axios.defaults.baseURL + 'uploaded/' + file.uuid" download>{{
      file.name
    }}</a>
  </div>
</template>
<style scoped></style>
