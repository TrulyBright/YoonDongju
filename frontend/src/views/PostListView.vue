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
      thereAreMore: false, // >> 버튼을 활성화해야 하는 경우
    };
  },
  watch: {
    async leftestIndex(newOffset, oldOffset) {
      await this.getRows();
    },
  },
  methods: {
    async getRows() {
      try {
        const result = await axios.get(
          `/${this.type}?skip=${
            Math.floor(this.offset / this.limit) * this.limit
          }&limit=${this.limit}`
        );
        this.items = result.data;
        const rest = await axios.get(
          `/${this.type}?skip=${
            Math.max(this.rightestIndex, 4) * this.rowPerPage
          }&limit=1`
        );
        this.thereAreMore = rest.data.length !== 0;
      } catch (error) {
        console.error(error);
      }
      console.log(
        this.offset,
        this.limit,
        this.paginationSpan,
        this.currentIndex,
        this.leftestIndex,
        this.rightestIndex
      );
      console.log(this.items);
    },
  },
  async created() {
    await this.getRows();
  },
  computed: {
    offset() {
      return this.$route.query.skip || 0;
    },
    limit() {
      return this.$route.query.limit || 50;
    },
    paginationSpan() {
      // pagination 가로줄 길이 (=칸 개수)
      return Math.floor(this.limit / this.rowPerPage);
    },
    // all below are 1-based index.
    currentIndex() {
      // 현재 보고 있는 pagination 칸 번호
      return Math.floor(this.offset / this.rowPerPage) + 1;
    },
    leftestIndex() {
      // pagination 가로줄의 맨 왼쪽 칸 번호
      return Math.floor(this.offset / this.limit) * this.paginationSpan + 1;
    },
    rightestIndex() {
      // pagination 가로줄의 맨 오른쪽 칸 번호
      return (
        this.leftestIndex -
        1 +
        Math.min(
          Math.ceil(this.items.length / this.rowPerPage),
          this.paginationSpan
        )
      );
    },
  },
};
</script>
<template>
  <main :key="items">
    <PostNavigator></PostNavigator>
    <ul class="list-group rounded">
      <PostOutlineItem
        v-for="item in items.slice(
          ((currentIndex % (paginationSpan + 1)) -
            1 +
            Math.floor(leftestIndex / paginationSpan)) *
            rowPerPage,
          ((currentIndex % (paginationSpan + 1)) +
            Math.floor(leftestIndex / paginationSpan)) *
            rowPerPage
        )"
        v-bind="item"
        :key="item"
        class="list-group-item"
      ></PostOutlineItem>
    </ul>
    <ListAction :type="type"></ListAction>
    <nav aria-label="Page navigation example">
      <ul class="pagination pagination-sm justify-content-center">
        <li
          :class="'page-item' + (leftestIndex === 1 ? ' disabled' : '')"
          :tabindex="leftestIndex === 1 ? '-1' : '0'"
        >
          <RouterLink
            class="page-link"
            :to="{
              path: 'notices',
              query: {
                skip: ((leftestIndex - 1) / paginationSpan - 1) * limit,
              },
            }"
            aria-label="Previous"
          >
            <span aria-hidden="true">&laquo;</span>
          </RouterLink>
        </li>
        <li
          :class="
            'page-item' +
            (leftestIndex + index === currentIndex ? ' active' : '')
          "
          v-for="index in [...Array(rightestIndex - leftestIndex + 1)].keys()"
          :key="index"
        >
          <RouterLink
            class="page-link"
            :to="{
              path: 'notices',
              query: { skip: (leftestIndex - 1 + index) * rowPerPage },
            }"
            >{{ leftestIndex + index }}</RouterLink
          >
        </li>
        <li
          :class="'page-item' + (thereAreMore ? '' : ' disabled')"
          :tabindex="thereAreMore ? '-1' : '0'"
        >
          <RouterLink
            class="page-link"
            :to="{
              path: 'notices',
              query: { skip: rightestIndex * rowPerPage },
            }"
            aria-label="Next"
          >
            <span aria-hidden="true">&raquo;</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
  </main>
</template>
<style scoped></style>
