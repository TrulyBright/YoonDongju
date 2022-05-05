<script setup>
import PostTitle from "./PostTitle.vue";
import axios from "axios";
import PostAction from "./PostAction.vue";
import PostMetadata from "./PostMetadata.vue";
import PostContent from "./PostContent.vue";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  components: { PostMetadata, PostContent },
  props: {
    name: String,
    conducted: String,
  },
  data() {
    return {
      topic: null,
      content: null,
      moderator: null,
    };
  },
  async created() {
    const response = await axios.get(
      "classes/" + this.name + "/records/" + this.conducted,
      {
        headers: {
          Authorization: store.authorizationHeader,
        },
      }
    );
    this.topic = response.data.topic;
    this.content = response.data.content;
    this.moderator = response.data.moderator;
  },
};
</script>
<template>
  <PostTitle v-if="topic" :title="topic"></PostTitle>
  <PostMetadata
    v-if="moderator"
    :author="moderator"
    :published="conducted"
    type="class-record"
  ></PostMetadata>
  <PostContent v-if="content" :content="content"></PostContent>
  <PostAction
    type="class-record"
    :className="name"
    :conducted="conducted"
    v-if="store.isAdmin"
  ></PostAction>
</template>
<style scoped></style>
