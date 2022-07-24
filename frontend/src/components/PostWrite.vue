<script setup>
// import PostInput from "@/components/PostInput.vue";
import PostPreview from "@/components/PostPreview.vue";
import { useMemberStore } from "../stores/member";
import axios from "axios";
import FileUploader from "./FileUploader.vue";
</script>
<script>
export default {
  props: {
    no: Number,
    type: String,
  },
  data() {
    return {
      form: {
        title: "",
        content: "",
        attached: [],
      },
      uploadProgress: 0,
      fileUploaderNextKey: 1,
      fileUploaderMap: {},
    };
  },
  async created() {
    if (!this.GETURI) return;
    const result = await axios.get(this.GETURI);
    this.form.title = result.data.title;
    this.form.content = result.data.content;
    this.form.attached = result.data.attached.map(item=>item.uuid);
    this.form.attached.forEach((uuid)=>{
      this.fileUploaderMap[this.fileUploaderNextKey++]=uuid;
    });
  },
  computed: {
    method() {
      switch (this.type) {
        case "about":
        case "rules":
          return axios.put;
        case "notices":
          return this.no === undefined ? axios.post : axios.patch;
        default:
          throw "unknown type: " + this.type;
      }
    },
    GETURI() {
      switch (this.type) {
        case "about":
        case "rules":
          return this.type;
        case "notices":
          return this.no === undefined ? null : `notices/${this.no}`;
        default:
          throw "unknown type: " + this.type;
      }
    },
    WriteURI() {
      switch (this.type) {
        case "about":
        case "rules":
          return this.type;
        case "notices":
          return this.no === undefined ? "notices" : `notices/${this.no}`;
        default:
          throw "unknown type: " + this.type;
      }
    },
  },
  methods: {
    routeToReturn(no) {
      switch (this.type) {
        case "about":
          return {
            name: "about",
          };
        case "rules":
          return {
            name: "rules",
          };
        case "notices":
          return {
            name: "notice",
            params: {
              no: no,
            },
          };
        default:
          throw "unknown type: " + this.type;
      }
    },
    fileUploaded(event) {
      this.form.attached.push(event.uuid);
    },
    fileRemoved(event) {
      this.form.attached = this.form.attached.filter(
        (item) => item !== event.uuid
      );
    },
    async submit() {
      try {
        const store = useMemberStore();
        const result = await this.method(this.WriteURI, this.form, {
          headers: {
            Authorization: store.authorizationHeader,
          },
        });
        this.$router.push(this.routeToReturn(result.data.no));
      } catch (error) {
        console.error(error);
      }
    },
    newUploader() {
      this.fileUploaderMap[this.fileUploaderNextKey++]="";
    },
  },
};
</script>
<template>
  <div class="container-fluid">
    <div class="row">
      <form class="col" @submit.prevent="submit">
        <div class="form-floating mb-1">
          <input
            type="text"
            class="form-control"
            id="title"
            v-model="form.title"
            placeholder="제목"
            required
          />
          <label for="title">제목</label>
        </div>
        <div class="form-floating mb-1">
          <textarea
            class="form-control"
            id="content"
            v-model="form.content"
            placeholder="본문"
            required
          ></textarea>
          <label for="content">본문</label>
        </div>
        <div>
          <label for="form-file-multiple"><small>첨부파일</small></label>
          <FileUploader
            @upload="fileUploaded"
            @uploadedRemove="fileRemoved"
            v-for="[key, uuid] of Object.entries(fileUploaderMap)"
            :key="key"
            :uuid="uuid"
            class="uploader"
          ></FileUploader>
          <button type="button" class="btn btn-light mt-1" @click="newUploader">
            첨부파일 추가
          </button>
        </div>
        <button type="submit" class="btn btn-light mt-1 d-none d-lg-block">
          게시
        </button>
      </form>
      <PostPreview :form="form" class="col d-none d-lg-block"></PostPreview>
    </div>
    <PostPreview :form="form" class="row d-lg-none"></PostPreview>
    <button type="button" class="btn btn-light mt-1 d-lg-none" @click="submit">
      게시
    </button>
  </div>
</template>
<style scoped>
textarea#content {
  min-height: 50vh;
}
</style>
