<script setup>
import axios from "axios";
import MagazineContents from "./MagazineContents.vue";
import { useMemberStore } from "../stores/member";
const store = useMemberStore();
</script>
<script>
export default {
  props: {
    cover: String,
    published: String,
  },
  data() {
    return {
      loading: false,
      item: null,
      error: null,
      showContents: false,
    };
  },
  async created() {
    this.error = this.item = null;
    this.loading = true;
    const response = await axios.get("magazines/" + this.published);
    this.item = {
      cover: response.data.cover,
      year: response.data.year,
      season: response.data.season,
      contents: response.data.contents,
      published: response.data.published,
    };
    this.loading = false;
  },
  computed: {
    contentsHeight() {
      return this.$el.querySelector("img.img-fluid").clientHeight;
    },
  },
  methods: {
    async deleteMagazine() {
      if (confirm(`${this.item.published}에 발간된 문집을 삭제합니다.`)) {
        await axios.delete("magazines/" + this.item.published, {
          headers: {
            Authorization: store.authorizationHeader,
          },
        });
        this.$router.go(); // refresh
      }
    },
  },
};
</script>
<template>
  <div class="card">
    <div v-if="loading" class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div v-if="error">{{ error }}</div>
    <div class="card-body" v-if="!loading && !error">
      <img
        :src="axios.defaults.baseURL + 'uploaded/' + item.cover"
        :alt="item.published + '에 발행된 문집 표지'"
        @click="showContents = true"
        v-if="!showContents"
        class="img-fluid"
      />
      <MagazineContents
        v-else
        :contents="item.contents"
        @close="showContents = false"
        class="contents"
        :style="`height:${contentsHeight}px;`"
      ></MagazineContents>
    </div>
    <div class="card-footer text-center" v-if="!loading && !error">
      {{ item.published }} 발행
      <i
        class="bi-gear"
        id="magazine-action"
        aria-expanded="false"
        data-bs-toggle="dropdown"
        v-if="store.isAdmin"
      ></i>
      <ul class="dropdown-menu" aria-labelledby="magazine-action">
        <li>
          <RouterLink
            :to="'/magazines/write?published=' + item.published"
            class="dropdown-item"
            >편집</RouterLink
          >
        </li>
        <li>
          <a @click="deleteMagazine" class="dropdown-item text-danger">삭제</a>
        </li>
      </ul>
    </div>
  </div>
</template>
<style>
i.bi-gear {
  cursor: pointer;
}
.dropdown-item {
  cursor: pointer;
}
img {
  cursor: pointer;
}
.card-body {
  overflow: auto;
}
</style>
