<script setup>
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
  <BButton :to="routeToWrite" v-if="store.isAdmin">글쓰기</BButton>
</template>
<style></style>
