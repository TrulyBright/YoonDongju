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
    canBe() {
      return this.roles.filter((val) => this.role !== val);
    },
  },
  methods: {
    async kick() {
      if (confirm(`이 회원(${this.student_id})을 사이트에서 추방합니다.`)) {
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
          `이 회원(${this.student_id})을 ${this.roleInKorean(english)}으로 ${
            this.roles.indexOf(english) > this.roles.indexOf(this.role)
              ? "승진"
              : "강등"
          }합니다.`
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
  <div>{{ username }}</div>
  <div>{{ real_name }}</div>
  <div>{{ student_id }}</div>
  <div>{{ roleInKorean(role) }}</div>
  <div>
    <BDropdown text="작업">
      <BDropdownHeader>권한 승강</BDropdownHeader>
      <BDropdownItem
        v-for="english in canBe"
        :key="english"
        @click="patch(english)"
        >{{ roleInKorean(english) }}으로</BDropdownItem
      >
      <BDropdownHeader>재적 변경</BDropdownHeader>
      <BDropdownItem @click="kick">추방</BDropdownItem>
    </BDropdown>
  </div>
</template>
<style scoped></style>
