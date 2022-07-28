<script setup>
import { useMemberStore } from "../stores/member";
import { Tooltip } from "bootstrap";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      loginForm: {
        username: null,
        password: null,
      },
      loginError: "",
      findIDForm: {
        portal_id: null,
        portal_pw: null,
      },
      IDFound: false,
      findIDResult: "",
      findPWForm: {
        portal_id: null,
        portal_pw: null,
        new_pw: null,
        new_pw_confirm: null,
      },
      PWFound: false,
      findPWResult: "",
    };
  },
  async created() {
    const tooltipTriggerList = document.querySelectorAll(
      '[data-bs-toggle="tooltip"]'
    );
    [...tooltipTriggerList].map(
      (tooltipTriggerEl) => new Tooltip(tooltipTriggerEl)
    );
  },
  methods: {
    async loginSubmit() {
      const spinner = document.querySelector("#login-loading");
      spinner.style.display = "inline-block";
      try {
        const store = useMemberStore();
        await store.requestToken(this.loginForm);
        await store.whoAmI();
        this.loginError = "";
        this.$emit("close");
        document.querySelector("#close-login-modal").click();
      } catch (e) {
        this.loginError = "계정명이나 비밀번호가 틀렸습니다.";
      }
      spinner.style.removeProperty("display");
    },
    async findIDFormSubmit() {
      const spinner = document.querySelector("#find-id-loading");
      spinner.style.display = "inline-block";
      try {
        const response = await axios.post("find-id", this.findIDForm);
        this.IDFound = true;
        this.findIDResult = response.data;
      } catch (e) {
        this.IDFound = false;
        if (e.message.includes("401")) {
          this.findIDResult = "해당 정보로 연세포탈에 접속할 수 없습니다.";
        } else if (e.message.includes("404")) {
          this.findIDResult = "가입되지 않은 학번입니다.";
        }
      }
      spinner.style.removeProperty("display");
    },
    async findPWFormSubmit() {
      if (!this.findPWFormValidate) {
        this.findPWResult = "새 비밀번호가 재입력된 것과 다릅니다.";
        return;
      }
      const spinner = document.querySelector("#find-pw-loading");
      spinner.style.display = "inline-block";
      try {
        await axios.post("find-pw", this.findPWForm);
        this.PWFound = true;
        this.findPWResult = "변경되었습니다! 새 비밀번호로 접속해주세요.";
      } catch (e) {
        this.PWFound = false;
        if (e.message.includes("401")) {
          this.findPWResult = "해당 정보로 연세포탈에 접속할 수 없습니다.";
        } else if (e.message.includes("404")) {
          this.findPWResult = "가입되지 않은 학번입니다.";
        } else if (e.message.includes("400")) {
          this.findPWResult = "비밀번호가 형식에 맞지 않습니다.";
        }
      }
      spinner.style.removeProperty("display");
    },
  },
  computed: {
    findPWFormValidate() {
      return this.findPWForm.new_pw === this.findPWForm.new_pw_confirm;
    },
  },
};
</script>
<template>
  <div class="modal fade" aria-hidden="true" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalToggleLabel">회원접속</h5>
          <button
            type="button"
            class="btn-close"
            id="close-login-modal"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="loginSubmit">
            <div class="form-floating mb-1">
              <input
                type="text"
                class="form-control"
                id="username-login"
                placeholder="계정명 ID"
                required
                v-model="loginForm.username"
              />
              <label for="username-login">계정명 ID</label>
            </div>
            <div class="form-floating mb-1">
              <input
                type="password"
                class="form-control"
                id="password-login"
                placeholder="비밀번호 Password"
                required
                v-model="loginForm.password"
              />
              <label for="password-login">비밀번호 Password</label>
            </div>
            <div>
              <button type="submit" class="btn btn-pink">
                접속
                <span
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                  id="login-loading"
                  ><span class="visually-hidden">인증 중...</span></span
                >
              </button>
              <span class="text-danger">{{ loginError }}</span>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-pink"
            data-bs-target="#forgot-id"
            data-bs-toggle="modal"
            data-bs-dismiss="modal"
          >
            계정명을 모르시나요?
          </button>
          <button
            class="btn btn-pink"
            data-bs-target="#forgot-pw"
            data-bs-toggle="modal"
            data-bs-dismiss="modal"
          >
            비밀번호를 모르시나요?
          </button>
        </div>
      </div>
    </div>
    <Teleport to="#app">
      <div
        class="modal fade"
        id="forgot-id"
        aria-hidden="true"
        aria-labelledby="exampleModalToggleLabel2"
        tabindex="-1"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalToggleLabel2">
                계정명 찾기
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="findIDFormSubmit">
                <p>
                  해당 연세포탈 ID로 가입된 계정이 있으면 계정명을 알려드립니다.
                </p>
                <div class="form-floating mb-1">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="연세포탈 ID"
                    required
                    v-model="findIDForm.portal_id"
                  />
                  <label for="username-login">연세포탈 ID</label>
                </div>
                <div class="form-floating mb-1">
                  <input
                    type="password"
                    class="form-control"
                    placeholder="연세포탈 비밀번호"
                    required
                    v-model="findIDForm.portal_pw"
                  />
                  <label for="password-login">연세포탈 비밀번호</label>
                </div>
                <div>
                  <button type="submit" class="btn btn-pink">
                    찾기
                    <span
                      class="spinner-border spinner-border-sm"
                      role="status"
                      aria-hidden="true"
                      id="find-id-loading"
                      ><span class="visually-hidden">찾는 중...</span></span
                    >
                  </button>
                  <span v-if="IDFound"
                    >계정명은 <span class="text-info">{{ findIDResult }}</span
                    >입니다.</span
                  >
                  <span class="text-danger" v-else>{{ findIDResult }}</span>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                class="btn btn-pink"
                data-bs-target="#login-modal"
                data-bs-toggle="modal"
                data-bs-dismiss="modal"
              >
                접속 창으로 돌아가기
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="modal fade"
        id="forgot-pw"
        aria-hidden="true"
        aria-labelledby="exampleModalToggleLabel2"
        tabindex="-1"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalToggleLabel2">
                비밀번호 찾기
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="findPWFormSubmit">
                <p>
                  해당 연세포탈 ID로 가입된 계정이 있으면 비밀번호가 변경됩니다.
                </p>
                <div class="form-floating mb-1">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="연세포탈 ID"
                    required
                    v-model="findPWForm.portal_id"
                  />
                  <label for="username-login">연세포탈 ID</label>
                </div>
                <div class="form-floating mb-1">
                  <input
                    type="password"
                    class="form-control"
                    placeholder="연세포탈 비밀번호"
                    required
                    v-model="findPWForm.portal_pw"
                  />
                  <label for="password-login">연세포탈 비밀번호</label>
                </div>
                <div class="form-floating mb-1">
                  <input
                    type="password"
                    class="form-control"
                    placeholder="새 비밀번호"
                    pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
                    data-bs-toggle="tooltip"
                    data-bs-placement="bottom"
                    title="10자 이상에 숫자와 영문이 하나씩은 있어야 합니다."
                    required
                    v-model="findPWForm.new_pw"
                  />
                  <label for="password-login">새 비밀번호</label>
                </div>
                <div class="form-floating mb-1">
                  <input
                    type="password"
                    class="form-control"
                    placeholder="새 비밀번호 재입력"
                    required
                    v-model="findPWForm.new_pw_confirm"
                  />
                  <label for="password-login">새 비밀번호 재입력</label>
                </div>
                <div>
                  <button type="submit" class="btn btn-pink">
                    변경
                    <span
                      class="spinner-border spinner-border-sm"
                      role="status"
                      aria-hidden="true"
                      id="find-pw-loading"
                      ><span class="visually-hidden">찾는 중...</span></span
                    >
                  </button>
                  <span class="text-info" v-if="PWFound">{{
                    findPWResult
                  }}</span>
                  <span class="text-danger" v-else>{{ findPWResult }}</span>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                class="btn btn-pink"
                data-bs-target="#login-modal"
                data-bs-toggle="modal"
                data-bs-dismiss="modal"
              >
                접속 창으로 돌아가기
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
<style scoped>
span.spinner-border {
  display: none;
}
</style>
