<script setup>
import { useMemberStore } from "../stores/member";
import { Tooltip } from "bootstrap";
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
      } catch (e) {
        this.loginError = "계정명이나 비밀번호가 틀렸습니다.";
      }
      spinner.style.removeProperty("display");
    },
  },
};
</script>
<template>
  <div
    class="modal fade"
    aria-hidden="true"
    aria-labelledby="exampleModalToggleLabel"
    tabindex="-1"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalToggleLabel">접속</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="loginSubmit">
            <div class="form-floating">
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
                ></span>
                <span class="visually-hidden">인증 중...</span>
              </button>
              <span class="text-danger">{{ loginError }}</span>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-pink"
            data-bs-target="#forgot-id-pw"
            data-bs-toggle="modal"
            data-bs-dismiss="modal"
          >
            계정명을 모르시나요?
          </button>
          <button
            class="btn btn-pink"
            data-bs-target="#forgot-id-pw"
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
        id="forgot-id-pw"
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
            <div class="modal-body">계정명을 입력하세요.</div>
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
