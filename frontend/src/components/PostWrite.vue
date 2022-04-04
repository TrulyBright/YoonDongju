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
        const member = useMemberStore().member;
        const result = await axios.patch("/notices/" + this.no, this.form, {
          headers: member.tokenType + " " + member.token,
        });
        this.$router.push({ name: result.data.type, params: { no: this.no } });
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
      />
    </div>
    <div>
      <textarea
        :value="form.content"
        @input="(event) => (form.content = event.target.value)"
      ></textarea>
    </div>
    <button type="submit">게시</button>
  </form>
  <PostPreview v-bind="content"></PostPreview>
</template>
<style scoped></style>
