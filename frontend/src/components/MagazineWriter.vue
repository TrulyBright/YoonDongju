<script setup>
import FileUploader from "./FileUploader.vue";
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
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
    };
  },
  async created() {
    if (!this.existingVolume) return;
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
          Authorization: useMemberStore().authorizationHeader,
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
    removeContent(content) {
      this.form.contents = this.form.contents.filter(
        (item) => item !== content
      );
    },
    onUpload(event) {
      this.form.cover = event.uuid;
      this.coverName = event.name;
    },
    onUploadRemove() {
      this.form.cover = null;
    },
  },
  computed: {
    existingVolume() {
      return typeof this.published === "string";
    },
    method() {
      return this.existingVolume ? axios.patch : axios.post;
    },
    URI() {
      return this.existingVolume ? "magazines/" + this.published : "magazines";
    },
    uploaded() {
      return this.form.cover !== null;
    },
  },
};
</script>
<template>
  <form @submit.prevent="submit">
    <h1>문집 {{ existingVolume ? "편집" : "추가" }}</h1>
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
      <div v-if="uploaded">
        <img
          :src="axios.defaults.baseURL + 'uploaded/' + form.cover"
          :alt="coverName"
          class="img-fluid mb-1"
          :key="form.cover"
        />
      </div>
      <FileUploader
        v-if="uploaded || !existingVolume"
        :uuid="form.cover"
        accept="image/*"
        name="cover"
        @upload="onUpload"
        @uploadRemove="onUploadRemove"
        class="w-100"
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
    <div class="input-group mb-3" id="basic-url">
      <label for="contents" class="form-label">수록작</label>
      <p class="d-none d-lg-block">네 번째 칸에서 Tab키를 눌러보세요.</p>
      <div
        v-for="[index, content] in form.contents.entries()"
        :key="content"
        class="row mb-1"
      >
        <input
          type="text"
          placeholder="르포르타주"
          v-model="content.type"
          class="form-control col me-1"
          required
        />
        <input
          type="text"
          placeholder="카탈로니아 찬가"
          v-model="content.title"
          class="form-control col me-1"
          required
        />
        <input
          type="text"
          placeholder="조지 오웰"
          v-model="content.author"
          class="form-control col me-1"
          required
        />
        <input
          type="text"
          placeholder="영어"
          v-model="content.language"
          @keydown.tab="
            if (index === form.contents.length - 1) addContentRow();
          "
          class="form-control col me-1"
          required
        />
        <button
          type="button"
          class="col btn btn-outline-danger"
          @click="removeContent(content)"
          tabIndex="-1"
        >
          삭제
        </button>
      </div>
      <button
        type="button"
        class="btn btn-outline-info rounded"
        @click="addContentRow"
      >
        추가
      </button>
    </div>
    <button type="submit" class="btn btn-primary">게시</button>
  </form>
</template>
<style scoped></style>
