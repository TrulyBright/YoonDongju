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
  <BTr>
    <BTd>{{ username }}</BTd>
    <BTd>{{ student_id }}</BTd>
    <BTd>{{ real_name }}</BTd>
    <BTd>{{ roleInKorean(role) }}</BTd>
    <BTd>
      <BDropdown text="작업" size="sm" class="action-dropdown">
        <BDropdownHeader>직책 승강</BDropdownHeader>
        <BDropdownItem
          v-for="english in roles"
          :key="english"
          :disabled="english === role"
          @click="patch(english)"
          >{{ roleInKorean(english) }}으로</BDropdownItem
        >
        <BDropdownDivider></BDropdownDivider>
        <BDropdownHeader>재적 변경</BDropdownHeader>
        <BDropdownItem @click="kick" variant="danger">추방</BDropdownItem>
      </BDropdown>
    </BTd>
  </BTr>
</template>
<style scoped>
.action-dropdown {
  position: static;
}
</style>
