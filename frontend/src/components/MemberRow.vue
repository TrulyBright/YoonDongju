<script setup>
import { useMemberStore } from "../stores/member";
import axios from "axios";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    username: String,
    real_name: String,
    student_id: String,
    role: String,
  },
  computed: {
    roles() {
      return ["member", "board", "president"];
    },
  },
  methods: {
    async kick() {
      if (confirm(`${this.real_name} 회원을 사이트에서 추방합니다.`)) {
        await axios.delete("members/" + this.student_id, {
          headers: {
            Authorization: store.authorizationHeader,
          },
        });
        this.$router.go();
      }
    },
    async patch(english) {
      if (
        confirm(
          `${this.real_name} 회원이 ${this.roleInKorean(english)}으로 ${
            this.roles.indexOf(english) > this.roles.indexOf(this.role)
              ? "승진"
              : "강등"
          }됩니다.`
        )
      ) {
        await axios.patch(
          "members/" + this.student_id,
          {
            role: english,
          },
          {
            headers: {
              Authorization: store.authorizationHeader,
            },
          }
        );
        this.$router.go();
      }
    },
    roleInKorean(english) {
      switch (english) {
        case "member":
          return "회원";
        case "board":
          return "임원";
        case "president":
          return "회장";
        default:
          return "불명";
      }
    },
  },
};
</script>
<template>
  <tr>
    <td>{{ student_id }}</td>
    <td>{{ real_name }}</td>
    <td>{{ roleInKorean(role) }}</td>
    <td>
      <i class="bi-gear" data-bs-toggle="dropdown" aria-expanded="false"></i>
      <ul class="dropdown-menu">
        <li class="dropdown-header">직책승강</li>
        <li
          v-for="english in roles"
          :key="english"
          :class="'dropdown-item ' + (english === role ? 'disabled' : '')"
          @click="patch(english)"
        >
          {{ roleInKorean(english) }}으로
        </li>
        <li class="dropdown-divider"></li>
        <li class="dropdown-header">재적변경</li>
        <li class="dropdown-item text-danger" @click="kick">추방</li>
      </ul>
    </td>
  </tr>
</template>
<style scoped>
i.bi-gear,
.dropdown-item {
  cursor: pointer;
}
.dropdown-menu {
  position: fixed !important;
}
</style>
