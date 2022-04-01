<script>
export default {
  props: {
    author: String,
    published: String,
    modifier: String,
    modified: String,
  },
};
</script>

<template>
  <div class="metadata">
    <div>글쓴이 {{ author }}</div>
    <div>게시일 {{ published }}</div>
    <div>수정자 {{ modifier }}</div>
    <div>수정일 {{ modified }}</div>
  </div>
</template>

<style scoped>
.metadata {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
</style>
