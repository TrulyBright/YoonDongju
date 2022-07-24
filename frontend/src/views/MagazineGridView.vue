<script setup>
import MagazineItem from "../components/MagazineItem.vue";
import axios from "axios";
import MagazineListAction from "../components/MagazineListAction.vue";
import { useMemberStore } from "../stores/member";
import PostNavigator from "../components/PostNavigator.vue";
const store = useMemberStore();
</script>
<script>
export default {
  data() {
    return {
      magazines: [],
    };
  },
  async created() {
    const response = await axios.get("magazines");
    this.magazines = response.data;
  },
};
</script>
<template>
  <div>
    <PostNavigator></PostNavigator>
    <h6>표지를 눌러보세요.</h6>
    <MagazineListAction v-if="store.isAdmin"></MagazineListAction>
    <MagazineItem
      v-for="volume in magazines"
      :key="volume.published"
      v-bind="volume"
    ></MagazineItem>
  </div>
</template>
<style></style>
