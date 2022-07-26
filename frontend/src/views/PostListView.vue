<script setup>
import axios from "axios";
import PostOutlineItem from "../components/PostOutlineItem.vue";
import ListAction from "../components/ListAction.vue";
import PostNavigator from "../components/PostNavigator.vue";
</script>
<script>
export default {
  props: {
    type: String,
  },
  data() {
    return {
      items: [],
      rowPerPage: 10, // 한번에 보이는 post 수
      total: 0,
    };
  },
  async created() {
    const response = await axios.get("notice-count");
    this.total = response.data;
    await this.getRows();
  },
  methods: {
    async getRows() {
      const itemsResponse = await axios.get(
        `notices?skip=${this.offset}&limit=${this.rowPerPage}`
      );
      this.items = itemsResponse.data;
    },
  },
  watch: {
    async offset() {
      await this.getRows();
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(
        (this.total - this.left * this.rowPerPage) / this.rowPerPage
      );
    },
    currentPage() {
      return Math.floor(this.offset / this.rowPerPage);
    },
    width() {
      return 5;
    },
    left() {
      return Math.max(
        0,
        Math.floor(this.offset / (this.rowPerPage * this.width)) * this.width
      );
    },
    generatePages() {
      return this.totalPages < this.width
        ? [...new Array(this.totalPages).keys()].map((item) => item + this.left)
        : [...new Array(this.width).keys()].map(
            (value, index) => index + this.left
          );
    },
    prevMore() {
      return this.generatePages[0] > 0;
    },
    nextMore() {
      return (
        this.generatePages[this.generatePages.length - 1] - this.left <
        this.totalPages - 1
      );
    },
    typeToRequest() {
      switch (this.type) {
        case "notices":
        case "notice":
          return "notices";
        default:
          throw "Type unknown to PostListView: " + this.type;
      }
    },
    offset() {
      return this.$route.query.skip || 0;
    },
  },
};
</script>
<template>
  <main>
    <PostNavigator></PostNavigator>
    <ul class="list-group rounded" :key="currentPage">
      <PostOutlineItem
        v-for="item in items"
        v-bind="item"
        :key="item"
        class="list-group-item"
      ></PostOutlineItem>
    </ul>
    <ListAction :type="type"></ListAction>
    <nav aria-label="Page navigation example">
      <ul class="pagination pagination-sm justify-content-center">
        <li v-if="prevMore" class="page-item">
          <RouterLink
            class="page-link"
            :to="{
              path: 'notices',
              query: { skip: offset - rowPerPage * width },
            }"
          >
            <span aria-hidden="true">&laquo;</span>
          </RouterLink>
        </li>
        <li v-for="page in generatePages" :key="page">
          <RouterLink
            :class="'page-link' + (currentPage === page ? ' active' : '')"
            :to="{ path: 'notices', query: { skip: rowPerPage * page } }"
            >{{ page + 1 }}</RouterLink
          >
        </li>
        <li v-if="nextMore" class="page-item">
          <RouterLink
            class="page-link"
            :to="{
              path: 'notices',
              query: { skip: (left + width) * rowPerPage },
            }"
          >
            <span aria-hidden="true">&raquo;</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
  </main>
</template>
<style scoped></style>
