<script setup>
import PostTitle from "./PostTitle.vue";
import PostContent from "./PostContent.vue";
import PostAttached from "./PostAttached.vue";
import PostMetadata from "./PostMetadata.vue";
</script>
<script>
export default {
  props: {
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
  ></PostMetadata>
  <PostContent :content="content"></PostContent>
  <PostAttached v-for="a in attached" :key="a.uuid" v-bind="a"></PostAttached>
</template>
