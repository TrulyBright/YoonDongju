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
  <div class="home">
    <div class="container-sm" id="front-image-container">
      <img
        src="@/assets/대문-그림.png"
        class="img-fluid"
        id="front-image"
        alt="어린 양이 연세문학회 문집으로 만든 굴에서 바깥으로 몸을 반쯤 내밀고 숨을 돌리고 있다."
      />
    </div>
    <div>
      <h3>
        <strong><RouterLink to="notices">공지</RouterLink></strong>
      </h3>
      <div class="recent-notices">
        <template v-for="notice in recentNotices" :key="notice">
          <RouterLink :to="{ name: 'notice', params: { no: notice.no } }">{{
            notice.title
          }}</RouterLink>
          <small class="date-published align-self-center">{{
            notice.published.split("-").slice(1).join("-")
          }}</small>
          <hr class="line-between-notices" />
        </template>
      </div>
    </div>
    <div>
      <h3>
        <strong><RouterLink to="magazines">문집</RouterLink></strong>
      </h3>
      <div
        id="carouselExampleInterval"
        class="carousel carousel-dark slide"
        data-bs-ride="carousel"
      >
        <div class="carousel-inner">
          <div
            :class="'carousel-item' + (index === 0 ? ' active' : '')"
            v-for="(magazine, index) in recentMagazines"
            :key="magazine"
            data-bs-interval="5000"
          >
            <img
              :src="axios.defaults.baseURL + 'uploaded/' + magazine.cover"
              class="img-fluid"
              :alt="magazine.published + '에 발간된 문집 표지'"
            />
          </div>
        </div>
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExampleInterval"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">전</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#carouselExampleInterval"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">후</span>
        </button>
      </div>
    </div>
  </div>
</template>
<style scoped>
#front-image-container {
  border-radius: 30px;
  padding: 1em;
  background: white;
}
.recent-notices {
  display: grid;
  grid-template-columns: 1fr auto;
}
hr.line-between-notices {
  grid-column: 1 / -1;
  margin: 0;
  border-top: 1px solid brown;
}
.home {
  display: grid;
  gap: 15px;
}
</style>
<style scoped>
a {
  color: var(--color-brown) !important;
}
</style>
