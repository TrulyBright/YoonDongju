<script setup>
import PostPreview from "@/components/PostPreview.vue";
import { useMemberStore } from "../stores/member";
import axios from "axios";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    name: String,
    conducted: [String, null],
  },
  data() {
    return {
      form: {
        conducted: "",
        topic: "",
        content: "",
        attached: [],
      },
    };
  },
  async created() {
    if (this.conducted !== null) {
      const response = await axios.get(
        "classes/" + this.name + "/records/" + this.conducted,
        {
          headers: {
            Authorization: store.authorizationHeader,
          },
        }
      );
      this.form.conducted = response.data.conducted;
      this.form.topic = response.data.topic;
      this.form.content = response.data.content;
    }
  },
  methods: {
    async submit() {
      const headers = {
        headers: {
          Authorization: store.authorizationHeader,
        },
      };
      const request =
        this.conducted !== null
          ? axios.patch(
              "classes/" + this.name + "/records/" + this.conducted,
              this.form,
              headers
            )
          : axios.post("classes/" + this.name + "/records", this.form, headers);
      const response = await request;
      this.$router.push({
        name: "classRecord",
        params: {
          name: response.data.class_name,
          conducted: response.data.conducted,
        },
      });
    },
  },
};
</script>
<template>
  <form @submit="submit">
    <input
      type="text"
      class="form-control"
      v-model="form.topic"
      placeholder="제목/주제"
    />
    <input
      type="date"
      class="form-control"
      v-model="form.conducted"
      placeholder="활동일자"
    />
    <textarea
      class="form-control"
      v-model="form.content"
      placeholder="본문"
    ></textarea>
    <button type="submit" class="btn btn-primary">게시</button>
  </form>
  <PostPreview :source="form.content"></PostPreview>
</template>
<style scoped></style>
