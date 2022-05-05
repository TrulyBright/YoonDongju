<script setup>
import axios from "axios";
import { RouterLink } from "vue-router";
</script>
<script>
export default {
  data() {
    return {
      recentNotices: [],
      recentMagazines: [],
    };
  },
  async created() {
    const [noticeResponse, magazineResponse] = await Promise.all([
      axios.get("recent-notices"),
      axios.get("recent-magazines"),
    ]);
    this.recentNotices = noticeResponse.data;
    this.recentMagazines = magazineResponse.data;
  },
};
</script>
<template>
  <BImg
    src="/대문 그림.jpg"
    fluid
    alt="연세문학회 문집 더미에 파묻힌 강아지가 바깥으로 몸을 반쯤 내밀고 숨을 돌리고 있다."
  ></BImg>
  <div>
    <RouterLink to="notices">공지</RouterLink>
    <div class="recent-notices">
      <div v-for="notice in recentNotices" :key="notice">
        <RouterLink :to="{ name: 'notice', params: { no: notice.no } }">{{
          notice.title
        }}</RouterLink>
        <div>{{ notice.published }}</div>
      </div>
    </div>
  </div>
  <div>
    <RouterLink to="magazines">문집</RouterLink>
    <div class="recent-magazines">
      <BImg
        fluid
        v-for="magazine in recentMagazines"
        :key="magazine"
        :src="axios.defaults.baseURL + 'uploaded/' + magazine.cover"
      ></BImg>
    </div>
  </div>
</template>
