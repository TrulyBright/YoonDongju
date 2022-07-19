<script setup>
import PostTitle from "./PostTitle.vue";
import PostContent from "./PostContent.vue";
import PostAttached from "./PostAttached.vue";
import PostMetadata from "./PostMetadata.vue";
import { useMemberStore } from "../stores/member";
const store = useMemberStore();
</script>
<script>
export default {
  props: {
    no: Number,
    type: String,
    title: String,
    content: String,
    published: String,
    author: String,
    modified: String,
    modifier: String,
    attached: Array,
  },
};
</script>

<template>
  <PostTitle :title="title"></PostTitle>
  <PostMetadata
    :author="author"
    :published="published"
    :modifier="modifier"
    :modified="modified"
    :type="type"
    :no="no"
    :isAdmin="store.isAdmin"
  ></PostMetadata>
  <PostContent :content="content"></PostContent>
  <hr />
  <PostAttached :data="attached"></PostAttached>
</template>
<style scoped>
.bi-gear {
  display: inline;
}
</style>
