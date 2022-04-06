<script setup>
import { RouterLink } from "vue-router";
import { useMemberStore } from "../stores/member";
const store = useMemberStore();
</script>
<script>
export default {
  props: {
    type: String,
  },
  computed: {
    routeToWrite() {
      switch (this.type) {
        case "notices":
          return {
            name: "writeNotice",
          };
        default:
          return undefined;
      }
    },
  },
};
</script>
<template>
  <RouterLink :to="routeToWrite" v-if="store.isAdmin">글쓰기</RouterLink>
</template>
<style></style>
