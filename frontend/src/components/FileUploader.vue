<script setup>
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    uuid: [String, null],
    accept: [String, null],
  },
  data() {
    return {
      input: null,
      uploaded: false,
    };
  },
  async created() {
    if (this.uuid) {
      console.log("before");
      const response = await axios.get("uploaded-info/" + this.uuid);
      console.log("after");
      console.log("after");
      this.applyUpload(response.data);
    }
  },
  methods: {
    applyUpload(data) {
      this.uploaded = true;
      this.$emit("upload", {
        name: data.name,
        uuid: data.uuid,
      });
    },
    async submit() {
      const formData = new FormData();
      formData.append("uploaded", this.input);
      const response = await axios.post("uploaded", formData, {
        headers: {
          Authorization: store.authorizationHeader,
        },
      });
      this.applyUpload(response.data);
    },
    changeFile(event) {
      const file = event.target.files[0];
      this.input = file;
    },
  },
};
</script>
<template>
  <form @submit="submit">
    <input
      type="file"
      class="form-control"
      @change="changeFile"
      :accept="accept"
    />
    <button type="submit" class="btn btn-primary">올리기/교체하기</button>
  </form>
</template>
<style scoped></style>
