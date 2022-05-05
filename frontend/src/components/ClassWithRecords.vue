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
  <BTableSimple hover small responsive>
    <BThead>
      <BTr>
        <BTh>주제</BTh>
        <BTh>분반장</BTh>
        <BTh>활동일</BTh>
      </BTr>
    </BThead>
    <BTbody>
      <BTr v-for="record in records" :key="record">
        <BTd>
          <RouterLink :to="this.name + '/' + record.conducted">{{
            record.topic
          }}</RouterLink></BTd
        >
        <BTd>{{ record.moderator }}</BTd>
        <BTd>{{ record.conducted }}</BTd>
      </BTr>
    </BTbody>
  </BTableSimple>
</template>
<style scoped>
th,
tr {
  text-align: center;
}
</style>
