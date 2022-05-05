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
  <BForm @submit="submit">
    <h1>문집 {{published ? "편집" : "추가"}}</h1>
    <BFormGroup label="연도">
      <BFormInput v-model="form.year" type="number" placeholder="2017" required></BFormInput>
    </BFormGroup>
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
    <BFormGroup label="발간일">
      <BFormInput v-model="form.published" type="date" required></BFormInput>
    </BFormGroup>
    <BFormGroup
      label-for="contents"
      label="수록작"
      description="마지막 칸에서 Tab키를 눌러보세요."
    >
      <div name="contents">
        <div v-for="content in form.contents" :key="content">
          <BFormInput
            type="text"
            placeholder="시, 소설, 희곡, 수필, ···"
            v-model="content.type"
            required
          ></BFormInput>
          <BFormInput
            type="text"
            placeholder="제목"
            v-model="content.title"
            required
          ></BFormInput>
          <BFormInput
            type="text"
            placeholder="작가"
            v-model="content.author"
            required
          ></BFormInput>
          <BFormInput
            type="text"
            placeholder="언어"
            v-model="content.language"
            @keydown.tab="addContentRow"
            required
          ></BFormInput>
          <BButton @click="removeContentRow(content)">제거</BButton>
        </div>
      </div>
    </BFormGroup>
    <BButton @click="addContentRow">수록작 추가</BButton>
    <BButton type="submit">게시</BButton>
  </BForm>
</template>
<style scoped></style>
