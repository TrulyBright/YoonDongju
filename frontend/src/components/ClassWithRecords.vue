<script setup>
import axios from "axios";
</script>
<script>
export default {
  props: {
    name: String,
  },
  data() {
    return {
      info: null,
      records: [],
    };
  },
  async created() {
    const [infoResponse, recordResponse] = await Promise.all([
      axios.get("classes/" + this.name),
      axios.get("classes/" + this.name + "/records"),
    ]);
    this.info = infoResponse.data;
    this.records = recordResponse.data;
  },
};
</script>
<template>
  <div v-if="info">
    <h1>{{ info.korean }}</h1>
    <div>
      <p>{{ info.moderator }}</p>
      <p>{{ info.schedule }}</p>
      <p>{{ info.description }}</p>
    </div>
  </div>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th>주제</th>
          <th>활동일</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="record in records" :key="record">
          <td>
            <RouterLink :to="this.name + '/' + record.conducted">
              {{ record.topic }}</RouterLink
            >
          </td>
          <td>{{ record.conducted }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<style scoped>
th,
tr {
  text-align: center;
}
</style>
