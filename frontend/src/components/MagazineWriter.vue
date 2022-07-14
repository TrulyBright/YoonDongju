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
        contents: [
          {
            type: null,
            title: null,
            author: null,
            language: null,
          },
        ],
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
  <form @submit="submit">
    <h1>문집 {{ published ? "편집" : "추가" }}</h1>
    <div class="input-group mb-3">
      <span class="input-group-text" id="label-year">연도</span>
      <input
        type="number"
        class="form-control"
        placeholder="1970"
        aria-label="year"
        v-model="form.year"
        aria-describedby="label-year"
        required
      />
    </div>
    <div class="input-group mb-3">
      <span class="input-group-text" id="label-cover">표지</span>
      <div v-if="published || uploaded">
        <img
          :src="axios.defaults.baseURL + 'uploaded/' + form.cover"
          :alt="coverName"
          class="img-fluid"
        />
      </div>
      <FileUploader
        :uuid="form.cover"
        accept="image/*"
        name="cover"
        @upload="onUpload"
      ></FileUploader>
    </div>
    <div class="input-group mb-3">
      <span class="input-group-text" id="label-published">발간일</span>
      <input
        type="date"
        class="form-control"
        placeholder="1970"
        aria-label="label-published"
        v-model="form.published"
        aria-describedby="label-published"
        required
      />
    </div>
    <label for="contents" class="form-label">수록작</label>
    <div class="input-group mb-3" id="basic-url">
      <div v-for="content in form.contents" :key="content">
        <input
          type="text"
          placeholder="시, 소설, 희곡, 수필, ···"
          v-model="content.type"
          class="form-control"
          required
        />
        <input
          type="text"
          placeholder="제목"
          v-model="content.title"
          class="form-control"
          required
        />
        <input
          type="text"
          placeholder="작가"
          v-model="content.author"
          class="form-control"
          required
        />
        <input
          type="text"
          placeholder="언어"
          v-model="content.language"
          @keydown.tab="addContentRow"
          class="form-control"
          required
        />
      </div>
    </div>
    <button type="submit" class="btn btn-primary">게시</button>
  </form>
</template>
<style scoped></style>
