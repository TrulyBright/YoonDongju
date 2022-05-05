<script>
export default {
  props: {
    author: String,
    published: String,
    modifier: String,
    modified: String,
    type: String,
  },
  computed: {
    isClassRecord() {
      return this.type === "class-record";
    },
  },
};
</script>

<template>
  <div class="metadata">
    <div>{{ isClassRecord ? "분반장" : "글쓴이" }} {{ author }}</div>
    <div>{{ isClassRecord ? "활동일" : "게시일" }} {{ published }}</div>
    <div v-if="!isClassRecord">수정자 {{ modifier }}</div>
    <div v-if="!isClassRecord">수정일 {{ modified }}</div>
  </div>
</template>

<style scoped>
.metadata {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
</style>
