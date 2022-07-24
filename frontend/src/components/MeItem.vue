<script setup>
import { useMemberStore } from "../stores/member";
import axios from "axios";
</script>
<script>
export default {
  props: {
    username: String,
    studentId: Number,
    realName: String,
    role: String,
  },
  methods: {
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
    async deleteAccountIfConfirmed() {
      if (
        confirm(
          "계정을 삭제하고 사이트에서 탈퇴하시겠습니까? 동아리 탈퇴는 따로 해야 합니다."
        )
      ) {
        const store = useMemberStore();
        await axios.delete(`/members/${this.studentId}`, {
          headers: {
            Authorization: store.authorizationHeader,
          },
        });
        store.logOut();
        this.$router.replace("/");
      }
    },
  },
};
</script>
<template>
  <form class="">
    <div class="mb-1 row">
      <label for="username" class="col-sm-2 col-form-label">계정명</label>
      <div class="col-sm-10">
        <input
          type="text"
          readonly
          class="form-control-plaintext"
          id="username"
          :value="username"
        />
      </div>
    </div>
    <div class="mb-1 row">
      <label for="student-id" class="col-sm-2 col-form-label">학번</label>
      <div class="col-sm-10">
        <input
          type="text"
          readonly
          class="form-control-plaintext"
          id="student-id"
          :value="studentId"
        />
      </div>
    </div>
    <div class="mb-1 row">
      <label for="real-name" class="col-sm-2 col-form-label">실명</label>
      <div class="col-sm-10">
        <input
          type="text"
          readonly
          class="form-control-plaintext"
          id="real-name"
          :value="realName"
        />
      </div>
    </div>
    <div class="mb-1 row">
      <label for="role" class="col-sm-2 col-form-label">직위</label>
      <div class="col-sm-10">
        <input
          type="text"
          readonly
          class="form-control-plaintext"
          id="role"
          :value="roleInKorean(role)"
        />
      </div>
    </div>
    <button
      type="button"
      class="btn btn-danger"
      @click="deleteAccountIfConfirmed"
    >
      계정 삭제
    </button>
  </form>
</template>
<style></style>
