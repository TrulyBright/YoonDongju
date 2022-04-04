<script setup>
import axios from "axios";
import MagazineCover from "./MagazineCover.vue";
import MagazineContents from "./MagazineContents.vue";
</script>
<script>
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
  </div>
</template>
<style></style>
