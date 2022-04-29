<script setup>
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    uuid: [String, null],
  },
  data() {
    return {
      input: null,
      uploaded: false,
      uploadedFileInfo: {
        name: null,
        uuid: null,
      },
    };
  },
  async created() {
    if (this.uuid) {
      const response = await axios.get("uploaded-info/" + this.uuid);
      this.uploaded = true;
      this.uploadedFileInfo.name = response.data.name;
      this.uploadedFileInfo.uuid = response.data.uuid;
      this.$emit("upload", this.uploadedFileInfo.uuid);
    }
  },
  methods: {
    async submit() {
      const formData = new FormData();
      formData.append("uploaded", this.input);
      const response = await axios.post("uploaded", formData, {
        headers: {
          Authorization: store.authorizationHeader,
        },
      });
      this.uploaded = true;
      this.uploadedFileInfo.name = response.data.name;
      this.uploadedFileInfo.uuid = response.data.uuid;
      this.$emit("upload", this.uploadedFileInfo.uuid);
    },
    changeFile(event) {
      const file = event.target.files[0];
      this.input = file;
    },
  },
};
</script>
<template>
  <div v-if="uploaded">
    <img
      :src="axios.defaults.baseURL + 'uploaded/' + uploadedFileInfo.uuid"
      :alt="uploadedFileInfo.name"
    />
    <div>
      {{ uploadedFileInfo.name }}
    </div>
  </div>
  <form @submit.prevent="submit">
    <input type="file" v-on:change="changeFile" />
    <input type="submit" value="올리기" />
  </form>
</template>
<style scoped></style>
