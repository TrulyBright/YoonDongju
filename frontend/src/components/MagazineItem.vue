<script setup>
import { RouterLink } from "vue-router";
import axios from "axios";
import MagazineCover from "./MagazineCover.vue";
import MagazineContents from "./MagazineContents.vue";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  components: {
    MagazineCover,
    MagazineContents,
  },
  props: {
    cover: String,
    published: String,
  },
  data() {
    return {
      loading: false,
      item: null,
      error: null,
      shown: "MagazineCover",
    };
  },
  created() {
    this.$watch(
      () => this.published,
      () => {
        this.fetchVolume();
      },
      { immediate: true }
    );
  },
  methods: {
    swap() {
      this.shown =
        this.shown === "MagazineCover" ? "MagazineContents" : "MagazineCover";
    },
    shownProperties() {
      return this.shown === "MagazineCover"
        ? { cover: this.item.cover, published: this.item.published }
        : { contents: this.item.contents };
    },
    fetchVolume() {
      this.error = this.item = null;
      this.loading = true;
      axios
        .get("/magazines/" + this.published)
        .then((response) => {
          this.item = {
            cover: response.data.cover,
            year: response.data.year,
            season: response.data.season,
            contents: response.data.contents,
            published: response.data.published,
          };
          this.loading = false;
        })
        .catch((error) => {
          this.error = error;
        });
    },
    async deleteMagazine(item) {
      if (confirm(`${item.published}에 발간된 문집을 삭제합니다.`)) {
        await axios.delete("magazines/" + item.published, {
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
  <div>
    <div v-if="loading">가져오는 중···</div>
    <div v-if="error">{{ error }}</div>
    <div @click="swap()">
      <component v-if="item" :is="shown" v-bind="shownProperties()"></component>
    </div>
    <div v-if="item && shown === 'MagazineCover'">
      <p>{{ item.year }}</p>
      <p>{{ item.season }}</p>
      <p>{{ item.published }}</p>
    </div>
    <RouterLink
      v-if="store.isAdmin"
      :to="'/magazines/write?published=' + item.published"
      >편집</RouterLink
    >
    <button type="button" v-if="store.isAdmin" @click="deleteMagazine(item)">
      삭제
    </button>
  </div>
</template>
<style></style>
