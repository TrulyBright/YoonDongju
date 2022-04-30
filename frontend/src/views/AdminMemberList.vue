<script setup>
import axios from "axios";
import { useMemberStore } from "../stores/member";
import MemberRow from "../components/MemberRow.vue";
</script>
<script>
const store = useMemberStore();
export default {
  data() {
    return {
      list: [],
    };
  },
  async created() {
    const response = await axios.get("members", {
      headers: {
        Authorization: store.authorizationHeader,
      },
    });
    this.list = response.data;
  },
};
</script>
<template>
  <BCard>
    <h2>명부</h2>
    <BTableSimple hover small caption-top responsive class="member-table">
      <BThead>
        <BTr>
          <BTh>ID</BTh>
          <BTh>학번</BTh>
          <BTh>실명</BTh>
          <BTh>직책</BTh>
          <BTh>작업</BTh>
        </BTr>
      </BThead>
      <BTbody>
        <MemberRow v-for="m in list" v-bind="m" :key="m.student_id"></MemberRow>
      </BTbody>
    </BTableSimple>
  </BCard>
</template>
<style scoped>
.member-table {
  overflow: visible;
}
</style>
