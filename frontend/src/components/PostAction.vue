<script setup>
import axios from "axios";
import { RouterLink } from "vue-router";
import { useMemberStore } from "../stores/member";
</script>
<script>
export default {
  props: {
    no: Number,
    type: String,
  },
  computed: {
    routeToWrite() {
      switch (this.type) {
        case "about":
          return {
            name: "writeAbout",
          };
        case "rules":
          return {
            name: "writeRules",
          };
        case "notices":
          return {
            name: "writeNotice",
            query: {
              no: this.no,
            },
          };
        default:
          throw "unknown type: " + this.type;
      }
    },
    routeToDelete() {
      switch (this.type) {
        case "notice":
          return `notices/${this.no}`;
        default:
          throw "unknown type: " + this.type;
      }
    },
  },
  methods: {
    async deleteIfConfirmed() {
      if (confirm("이 글을 삭제합니다.")) {
        try {
          await axios.delete(this.routeToDelete, {
            headers: {
              Authorization: useMemberStore().authorizationHeader,
            },
          });
          this.$router.push("/notices");
        } catch (error) {
          console.error(error);
        }
      }
    },
  },
};
</script>
<template>
  <div>
    <RouterLink :to="routeToWrite">수정</RouterLink>
    <button @click="deleteIfConfirmed">삭제</button>
  </div>
</template>
<style></style>
