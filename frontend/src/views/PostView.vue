<script setup>
import PostItem from "@/components/PostItem.vue";
import axios from "axios";
</script>
<script>
export default {
  props: {
    type: String,
    no: Number,
  },
  data() {
    return {
      post: {
        title: "",
        content: "",
        published: "",
        author: "",
        modifier: null,
        modified: null,
        attached: [],
      },
    };
  },
  created() {
    let route = null;
    switch (this.type) {
      case "about":
        route = "about";
        break;
      case "rules":
        route = "rules";
        break;
      case "notice":
        route = "notices/" + this.no;
        break;
    }
    axios
      .get(route)
      .then((res) => {
        this.post.no = res.data.no;
        this.post.title = res.data.title;
        this.post.content = res.data.content;
        this.post.published = res.data.published;
        this.post.author = res.data.author;
        this.post.modifier = res.data.modifier;
        this.post.modified = res.data.modified;
        this.post.attached = res.data.attached;
      })
      .catch((error) => {
        switch (error.response.status) {
          case 404:
            // TODO
            break;

          default:
            console.error(error);
            break;
        }
      });
  },
};
</script>
<template>
  <main>
    <PostItem v-bind="post"></PostItem>
  </main>
</template>

<style></style>
