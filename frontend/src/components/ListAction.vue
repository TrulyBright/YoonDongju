<script setup>
import { RouterLink } from "vue-router";
import { useMemberStore } from "../stores/member";
const store = useMemberStore();
</script>
<script>
export default {
  props: {
    routeName: String,
  },
  computed: {
    writingLink() {
      return this.routeName === "class" ? "classWrite" : "write";
    },
  },
};
</script>
<template>
  <RouterLink :to="writingLink" v-if="store.isAdmin">글쓰기</RouterLink>
</template>
<style></style>
