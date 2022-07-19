<script setup>
import { useMemberStore } from "../stores/member";
import axios from "axios";
const store = useMemberStore();
</script>
<script>
export default {
  props: {
    author: String,
    published: String,
    modifier: String,
    modified: String,
    type: String,
    className: [String, null],
    conducted: [String, null],
    no: Number,
  },
  computed: {
    isClassRecord() {
      return this.type === "class-record";
    },
    routeToWrite() {
      switch (this.type) {
        case "about":
          return {
            name: "writeAbout",
          };
        case "rules":
          return {
            name: "writeRules",
          };
        case "notices":
          return {
            name: "writeNotice",
            query: {
              no: this.no,
            },
          };
        case "class-record":
          return {
            name: "writeClassRecord",
            params: {
              name: this.className,
            },
            query: {
              conducted: this.conducted,
            },
          };
        default:
          throw "unknown type to set PostAction for: " + this.type;
      }
    },
    routeToDelete() {
      switch (this.type) {
        case "notice":
        case "notices":
          return `notices/${this.no}`;
        default:
          throw "unknown type: " + this.type;
      }
    },
  },
  methods: {
    async deleteIfConfirmed() {
      if (confirm("이 글을 삭제합니다.")) {
        try {
          await axios.delete(this.routeToDelete, {
            headers: {
              Authorization: useMemberStore().authorizationHeader,
            },
          });
          this.$router.push("/notices");
        } catch (error) {
          console.error(error);
        }
      }
    },
  },
};
</script>

<template>
  <div class="container metadata">
    <div class="row row-cols-auto">
      <small class="col">{{ author }}</small>
      <small class="col">{{ published }}</small>
      <i
        class="bi-gear"
        id="action-for-post"
        data-bs-toggle="dropdown"
        aria-expanded="false"
        v-if="store.isAdmin"
      >
      </i>
      <ul class="dropdown-menu" aria-labelledby="action-for-post">
        <RouterLink class="dropdown-item" :to="routeToWrite">수정</RouterLink>
        <button
          class="dropdown-item"
          id="delete-button"
          @click="deleteIfConfirmed"
          v-if="type !== 'about' && type !== 'rules'"
        >
          삭제
        </button>
      </ul>
      <small class="col" v-if="!isClassRecord">{{ modifier }}</small>
      <small class="col" v-if="!isClassRecord">{{ modified }}</small>
    </div>
  </div>
</template>

<style scoped>
.container.metadata {
  padding-left: unset;
  margin-left: unset;
}
#action-for-post {
  cursor: pointer;
  font-size: 14px;
}
#delete-button {
  color: red;
}
</style>
