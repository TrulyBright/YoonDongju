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
    type: String,
  },
  data() {
    return {
      form: {
        title: "",
        content: "",
        attached: [],
        attachedScheduled: [],
      },
    };
  },
  async created() {
    if (!this.GETURI) return;
    try {
      const result = await axios.get(this.GETURI);
      this.form.title = result.data.title;
      this.form.content = result.data.content;
      this.form.attached = result.data.attached;
    } catch (error) {
      console.error(error);
    }
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
    async submit() {
      try {
        const store = useMemberStore();
        const uploadPromises = [];
        for (const [index, file] of Object.entries(
          this.form.attachedScheduled
        )) {
          const formData = new FormData();
          formData.append("uploaded", file);
          uploadPromises.push(
            axios.post("uploaded", formData, {
              headers: {
                Authorization: store.authorizationHeader,
              },
            })
          );
        }
        const uploadResponses = await Promise.all(uploadPromises);
        this.form.attached = [];
        uploadResponses.forEach((response) => {
          this.form.attached.push(response.data.uuid);
        });
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
    updateAttached(event) {
      this.form.attachedScheduled = event.target.files;
    },
  },
};
</script>
<template>
  <div class="container-fluid">
    <div class="row">
      <form class="col">
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
          <label for="form-file-multiple"
            ><small>첨부파일(여러 개 올릴 수 있습니다)</small></label
          >
          <input
            type="file"
            id="form-file-multiple"
            class="form-control form-control-sm"
            @change="updateAttached"
            multiple
          />
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
