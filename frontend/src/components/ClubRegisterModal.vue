<script setup>
import { Toast } from "bootstrap";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      registerForm: {
        portal_id: null,
        portal_pw: null,
        tel: null,
        invite_informal_chat: null,
      },
      registerError: "",
    };
  },
  methods: {
    async registerSubmit() {
      const spinner = document.querySelector("#club-register-loading");
      spinner.style.display = "inline-block";
      try {
        await axios.post("/club-members", this.registerForm);
        this.registerError = "";
        this.$router.push({ name: "home" });
        document.querySelector("#close-club-register-modal").click();
        new Toast(document.getElementById("club-register-success")).show();
      } catch (error) {
        this.registerError = `${error.response.status}: ${error.response.data.detail}`;
      }
      spinner.style.removeProperty("display");
    },
  },
};
</script>
<template>
  <div class="modal fade" aria-hidden="true" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalToggleLabel">
            동아리 회원가입
          </h5>
          <button
            type="button"
            class="btn-close"
            id="close-club-register-modal"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>사이트 회원가입은 따로 하셔야 합니다.</p>
          <form @submit.prevent="registerSubmit">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                id="club-register-portal-id"
                v-model="registerForm.portal_id"
                placeholder="신촌캠 학부 학번"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                pattern="^[0-9]{4}1[0-9]{5}$"
                title="학부 시절의 학번을 입력하셔야 합니다."
                required
              />
              <label for="club-register-portal-id">신촌캠 학부 학번</label>
            </div>
            <small
              >학번이 숫자 10자리가 아닌가요? 관리자에게
              <a href="mailto:trulybright@yonsei.ac.kr">문의</a>하세요.</small
            >
            <div class="form-floating">
              <input
                type="password"
                class="form-control"
                id="club-register-portal-pw"
                v-model="registerForm.portal_pw"
                placeholder="연세포탈 비밀번호"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="저장되지 않고, 신촌캠 구성원 확인에만 일회용됩니다."
                required
              />
              <label for="club-register-portal-pw">연세포탈 비밀번호</label>
            </div>
            <div class="form-floating">
              <input
                type="tel"
                class="form-control"
                id="club-register-tel"
                v-model="registerForm.tel"
                placeholder="초대받을 전화번호"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="이 번호로 단톡방에 초대됩니다."
                required
              />
              <label for="club-register-tel">전화번호</label>
            </div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="club-register-invite-informal-chat"
                v-model="registerForm.invite_informal_chat"
                placeholder="잡담방 초대 여부"
                checked
              />
              <label
                for="club-register-invite-informat-chat"
                class="form-check-label"
                >잡담방에 초대를 받습니다.</label
              >
            </div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="club-register-agreement"
                required
              />
              <label for="club-register-agreement" class="form-check-label"
                >입력한 정보로 학사정보(실명/학번/전공/재적구분)를 받아오는 데
                동의합니다.</label
              >
            </div>
            <div>
              <button type="submit" class="btn btn-pink">
                가입<span
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                  id="club-register-loading"
                  ><span class="visually-hidden">가입 중...</span></span
                >
              </button>
              <span class="text-danger">{{ registerError }}</span>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
#club-register-loading {
  display: none;
}
</style>
