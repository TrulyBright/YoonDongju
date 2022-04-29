<script setup>
import MagazineItem from "../components/MagazineItem.vue";
import axios from "axios";
import MagazineListAction from "../components/MagazineListAction.vue";
import { useMemberStore } from "../stores/member";
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
    <MagazineListAction v-if="store.isAdmin"></MagazineListAction>
    <MagazineItem
      v-for="volume in magazines"
      :key="volume.published"
      v-bind="volume"
    ></MagazineItem>
  </div>
</template>
<style></style>
