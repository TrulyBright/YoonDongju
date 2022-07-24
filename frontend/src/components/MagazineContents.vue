<script setup>
import MagazineContent from "./MagazineContent.vue";
</script>
<script>
export default {
  props: {
    contents: Array,
  },
};
</script>
<template>
  <div>
    <div class="container text-center">
      <strong class="col align-self-center">수록작</strong>
      <button type="button" class="btn-close" @click="$emit('close')"></button>
    </div>
    <div class="rows">
      <MagazineContent
        v-for="content in contents"
        :key="content"
        v-bind="content"
        class="row"
      ></MagazineContent>
    </div>
  </div>
</template>
<style>
.rows {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 5px;
}
button.btn-close {
  position: absolute;
  right: 0;
}
</style>
