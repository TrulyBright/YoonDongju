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
    student_id: Number,
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
      <div class="dropdown">
        <button
          type="button"
          class="btn btn-secondary dropdown-toggle"
          data-bs-toggle="action-dropdown"
          aria-expanded="false"
        >
          작업
        </button>
        <ul class="dropdown-menu">
          <li><h6 class="dropdown-header">직책승강</h6></li>
          <li v-for="english in roles" :key="english">
            <button
              type="button"
              :class="'dropdown-item ' + (english === role ? 'disabled' : '')"
              @click="patch(english)"
            >
              {{ roleInKorean(english) }}으로
            </button>
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><h6 class="dropdown-header">재적변경</h6></li>
          <li>
            <button
              type="button"
              @click="kick"
              class="dropdown-item btn-danger"
            >
              추방
            </button>
          </li>
        </ul>
      </div>
    </td>
  </tr>
</template>
<style scoped></style>
