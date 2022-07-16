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
  <div class="container metadata">
    <div class="row row-cols-auto">
      <small class="col">{{ author }}</small>
      <small class="col">{{ published }}</small>
      <small class="col" v-if="!isClassRecord">{{ modifier }}</small>
      <small class="col" v-if="!isClassRecord">{{ modified }}</small>
    </div>
  </div>
</template>

<style scoped>
.container.metadata {
  padding-left: unset;
  margin-left: unset;
}
</style>
