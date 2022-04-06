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
