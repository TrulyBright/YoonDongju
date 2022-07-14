<script setup>
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
  <div>
    <div v-if="loading" class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div v-if="error">{{ error }}</div>
    <div @click="swap()">
      <component v-if="item" :is="shown" v-bind="shownProperties()"></component>
    </div>
    <div v-if="item && shown === 'MagazineCover'">
      <p>{{ item.year }}</p>
      <p>{{ item.season }}</p>
      <p>{{ item.published }}</p>
    </div>
    <div class="dropdown" v-if="item && store.isAdmin">
      <button
        class="btn btn-secondary dropdown-toggle"
        type="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        작업
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li>
          <RouterLink
            :to="'/magazines/write?published=' + item.published"
            class="dropdown-item"
            >편집</RouterLink
          >
        </li>
        <li>
          <a @click="deleteMagazine" href="#" class="dropdown-item">삭제</a>
        </li>
      </ul>
    </div>
  </div>
</template>
<style></style>
