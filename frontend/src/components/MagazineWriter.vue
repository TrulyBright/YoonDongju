<script setup>
import FileUploader from "./FileUploader.vue";
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    published: String,
  },
  data() {
    return {
      form: {
        year: null,
        cover: null,
        published: null,
        contents: [],
      },
      coverName: null,
      uploaded: false,
    };
  },
  async created() {
    const response = await axios.get("magazines/" + this.published);
    this.form.year = response.data.year;
    this.form.cover = response.data.cover;
    this.form.published = response.data.published;
    this.form.contents = response.data.contents;
  },
  methods: {
    async submit() {
      console.log(this.form);
      await this.method(this.URI, this.form, {
        headers: {
          Authorization: store.authorizationHeader,
        },
      });
      this.$router.push({
        name: "magazines",
      });
    },
    addContentRow() {
      this.form.contents.push({
        type: null,
        title: null,
        author: null,
        language: null,
      });
    },
    removeContentRow(content) {
      this.form.contents = this.form.contents.filter(
        (item) => item !== content
      );
    },
    onUpload(event) {
      this.form.cover = event.uuid;
      this.coverName = event.name;
      this.uploaded = true;
    },
  },
  computed: {
    method() {
      return this.published ? axios.patch : axios.post;
    },
    URI() {
      return this.published ? "magazines/" + this.published : "magazines";
    },
  },
};
</script>
<template>
  <form @submit.prevent="submit">
    <label for="year"
      >연도<input
        type="number"
        :value="form.year"
        @input="(event) => (form.year = event.target.value)"
        required
    /></label>
    <label for="cover"
      >표지
      <div v-if="published || uploaded">
        <img
          :src="axios.defaults.baseURL + 'uploaded/' + form.cover"
          :alt="coverName"
        />
      </div>
      <FileUploader
        :uuid="form.cover"
        accept="image/*"
        name="cover"
        @upload="onUpload"
      ></FileUploader>
    </label>
    <label for="published"
      >발간일<input
        type="date"
        name="published"
        :value="form.published"
        @input="(event) => (form.published = event.target.value)"
        required
    /></label>
    <label for="contents"
      >수록작
      <div name="contents">
        <li v-for="content in form.contents" :key="content">
          <input
            type="text"
            placeholder="시, 소설, 희곡, 수필, ···"
            :value="content.type"
            @input="(event) => (content.type = event.target.value)"
          />
          <input
            type="text"
            placeholder="제목"
            :value="content.title"
            @input="(event) => (content.title = event.target.value)"
          />
          <input
            type="text"
            placeholder="작가"
            :value="content.author"
            @input="(event) => (content.author = event.target.value)"
          />
          <input
            type="text"
            placeholder="언어"
            :value="content.language"
            @input="(event) => (content.language = event.target.value)"
          />
          <button type="button" @click="removeContentRow(content)">삭제</button>
        </li>
      </div>
      <button type="button" @click="addContentRow">수록작 추가</button>
    </label>
    <input type="submit" value="게시" />
  </form>
</template>
<style scoped></style>
