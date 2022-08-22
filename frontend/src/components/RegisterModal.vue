<script setup>
import { useMemberStore } from "../stores/member";
import { Tooltip } from "bootstrap";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      registerForm: {
        portal_id: null,
        portal_pw: null,
        username: null,
        password: null,
        passwordConfirm: null,
      },
      registerError: "",
    };
  },
  async created() {
    const response = await axios.get("classes");
    this.classes = response.data;
    const tooltipTriggerList = document.querySelectorAll(
      '[data-bs-toggle="tooltip"]'
    );
    [...tooltipTriggerList].map(
      (tooltipTriggerEl) => new Tooltip(tooltipTriggerEl)
    );
  },
  methods: {
    async registerSubmit() {
      const spinner = document.querySelector("#register-loading");
      spinner.style.display = "inline-block";
      if (this.validate()) {
        try {
          await useMemberStore().register(this.registerForm);
          this.registerError = "";
          this.$router.push({ name: "home" });
          document.querySelector("#close-register-modal").click();
        } catch (error) {
          this.registerError = `${error.response.status}: ${error.response.data.detail}`;
        }
      }
      spinner.style.removeProperty("display");
    },
    validate() {
      if (this.registerForm.password === this.registerForm.passwordConfirm) {
        this.registerError = "";
        return true;
      }
      this.registerError = "재입력된 비밀번호가 다릅니다.";
      return false;
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
            사이트 회원가입
          </h5>
          <button type="button" class="btn-close" id="close-register-modal" data-bs-dismiss="modal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>동아리 회원가입은 따로 하셔야 합니다.</p>
          <form @submit.prevent="registerSubmit">
            <div class="form-floating">
              <input type="text" class="form-control" id="portal-id" v-model="registerForm.portal_id"
                pattern="^[0-9]{4}1[0-9]{5}$" placeholder="신촌캠 학부 학번" data-bs-toggle="tooltip"
                data-bs-placement="bottom" title="학부 시절의 학번을 입력하셔야 합니다." required />
              <label for="portal-id">신촌캠 학부 학번</label>
            </div>
            <div class="form-floating">
              <input type="password" class="form-control" id="portal-pw" v-model="registerForm.portal_pw"
                placeholder="연세포탈 비밀번호" data-bs-toggle="tooltip" data-bs-placement="bottom"
                title="저장되지 않고, 신촌캠 구성원 확인에만 일회용됩니다." required />
              <label for="portal-pw">연세포탈 비밀번호</label>
            </div>
            <div class="form-floating">
              <input type="text" class="form-control" id="username" v-model="registerForm.username"
                placeholder="사용할 계정명 (ID)" pattern="^.{1,65}$" required data-bs-toggle="tooltip"
                data-bs-placement="bottom" title="최대 64자에, 한글을 비롯하여 어떤 문자든 허용됩니다." />
              <label for="username">사용할 계정명 (ID)</label>
            </div>
            <div class="form-floating">
              <input type="password" class="form-control" id="password" v-model="registerForm.password"
                placeholder="사용할 비밀번호" pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$" data-bs-toggle="tooltip"
                data-bs-placement="bottom" title="10자 이상에 숫자와 영문이 하나씩은 있어야 합니다." required />
              <label for="password">사용할 비밀번호</label>
            </div>
            <div class="form-floating mb-2">
              <input type="password" class="form-control" id="password-confirm" placeholder="사용할 비밀번호 재입력"
                v-model="registerForm.passwordConfirm" required />
              <label for="password-confirm">사용할 비밀번호 재입력</label>
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" id="register-agreement" required />
              <label for="register-agreement" class="form-check-label">입력한 정보로 학사정보(실명)를 받아오는 데
                동의합니다.</label>
            </div>
            <div>
              <button type="submit" class="btn btn-pink">
                가입<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"
                  id="register-loading"><span class="visually-hidden">가입 중...</span></span>
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
#register-loading {
  display: none;
}
</style>
