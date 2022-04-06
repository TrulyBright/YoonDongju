<script setup>
// import PostInput from "@/components/PostInput.vue";
import PostPreview from "@/components/PostPreview.vue";
import { useMemberStore } from "../stores/member";
import axios from "axios";
</script>
<script>
export default {
  props: {
    no: Number,
  },
  data() {
    return {
      form: {
        title: "",
        content: "",
        attached: [],
      },
    };
  },
  async created() {
    if (!this.no) return;
    try {
      let result = await axios.get("/notices/" + this.no);
      this.form.title = result.data.title;
      this.form.content = result.data.content;
      this.form.attached = result.data.attached;
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async submit() {
      try {
        const store = useMemberStore();
        const method = this.no === undefined ? axios.post : axios.patch;
        const URI = this.no === undefined ? "notices" : `notices/${this.no}`;
        const result = await method(URI, this.form, {
          headers: {
            Authorization: store.authorizationHeader,
          },
        });
        this.$router.push({
          name: result.data.type,
          params: { no: result.data.no },
        });
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
<template>
  <form @submit.prevent="submit">
    <!-- <PostInput>
      <template #title>{{ title }}</template>
      <template #content>{{ content }}</template>
    </PostInput> -->
    <div>
      <input
        :value="form.title"
        @input="(event) => (form.title = event.target.value)"
        placeholder="제목"
      />
    </div>
    <div>
      <textarea
        :value="form.content"
        @input="(event) => (form.content = event.target.value)"
        placeholder="본문"
      ></textarea>
    </div>
    <button type="submit">게시</button>
  </form>
  <PostPreview :source="form.content"></PostPreview>
</template>
<style scoped></style>
