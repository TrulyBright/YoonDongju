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
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">명부</h5>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>학번</th>
              <th>실명</th>
              <th>직책</th>
              <th>작업</th>
            </tr>
          </thead>
          <tbody>
            <MemberRow
              v-for="m in list"
              v-bind="m"
              :key="m.student_id"
            ></MemberRow>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
