<script setup>
import axios from "axios";
import { RouterLink } from "vue-router";
import { useMemberStore } from "../stores/member";
</script>
<script>
export default {
  props: {
    no: Number,
  },
  methods: {
    async deleteIfConfirmed() {
      if (confirm("이 글을 삭제합니다.")) {
        try {
          await axios.delete("/notices/" + this.no, {
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
    <RouterLink :to="{ name: 'write', query: { no: no } }">수정</RouterLink>
    <button @click="deleteIfConfirmed">삭제</button>
  </div>
</template>
<style></style>
