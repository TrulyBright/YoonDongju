<script setup>
import axios from "axios";
import PostOutlineItem from "../components/PostOutlineItem.vue";
import ListAction from "../components/ListAction.vue";
import PostNavigator from "../components/PostNavigator.vue";
</script>
<script>
export default {
  props: {
    type: String,
  },
  data() {
    return {
      items: [],
    };
  },
  async created() {
    try {
      const result = await axios.get(
        `/${this.type}?skip=` +
          (this.$route.query.skip || 0) +
          "&limit=" +
          (this.$route.query.limit || 20)
      );
      this.items = result.data;
    } catch (error) {
      console.error(error);
    }
  },
};
</script>
<template>
  <main>
    <PostNavigator></PostNavigator>
    <PostOutlineItem
      v-for="item in items"
      v-bind="item"
      :key="item"
    ></PostOutlineItem>
    <ListAction :type="type"></ListAction>
  </main>
</template>
<style scoped></style>
