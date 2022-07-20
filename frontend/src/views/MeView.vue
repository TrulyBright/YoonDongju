<script setup>
import { useMemberStore } from "../stores/member";
import MeItem from "../components/MeItem.vue";
</script>
<script>
export default {
  data() {
    return {
      member: null,
    };
  },
  async created() {
    this.member = await useMemberStore().whoAmI();
  },
};
</script>
<template>
  <MeItem v-bind="member"></MeItem>
</template>
<style></style>
