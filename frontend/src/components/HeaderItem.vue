<script setup>
import { useMemberStore } from "../stores/member";
import { Tooltip } from "bootstrap";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      openLoginForm: false,
      store: useMemberStore(),
      classes: [],
      loginForm: {
        username: null,
        password: null,
      },
      registerForm: {
        portal_id: null,
        portal_pw: null,
        real_name: null,
        username: null,
        password: null,
        passwordConfirm: null,
      },
      loginError: "",
      registerError: "",
      repeated: "",
      confirmElement: null,
    };
  },
  props: {
    address: String,
    email: String,
    presidentName: String,
    presidentTel: String,
    joinFormUrl: String,
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
    async submit() {
      const store = useMemberStore();
      await store.requestToken(this.loginForm);
      await store.whoAmI();
    },
  },
};
</script>
<template>
  <div
    class="modal fade"
    id="login-modal"
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
          <form @submit.prevent="submit">
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
            <button type="submit" class="btn btn-light">접속</button>
          </form>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-light"
            data-bs-target="#forgot-id-pw"
            data-bs-toggle="modal"
            data-bs-dismiss="modal"
          >
            계정명을 모르시나요?
          </button>
          <button
            class="btn btn-light"
            data-bs-target="#forgot-id-pw"
            data-bs-toggle="modal"
            data-bs-dismiss="modal"
          >
            비밀번호를 모르시나요?
          </button>
        </div>
      </div>
    </div>
  </div>
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
          <h5 class="modal-title" id="exampleModalToggleLabel2">계정명 찾기</h5>
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
            class="btn btn-light"
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
    id="register-modal"
    aria-hidden="true"
    aria-labelledby="exampleModalToggleLabel"
    tabindex="-1"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalToggleLabel">
            사이트 회원가입
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>동아리 회원가입은 따로 하셔야 합니다.</p>
          <form @submit="submit">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                id="portal-id"
                v-model="registerForm.portal_id"
                placeholder="연세포탈 ID"
                required
              />
              <label for="portal-id">연세포탈 ID</label>
            </div>
            <div class="form-floating">
              <input
                type="password"
                class="form-control"
                id="portal-pw"
                v-model="registerForm.portal_pw"
                placeholder="연세포탈 비밀번호"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="저장되지 않고, 신촌캠 구성원 확인에만 일회용됩니다."
                required
              />
              <label for="portal-pw">연세포탈 비밀번호</label>
            </div>
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                id="real-name"
                v-model="registerForm.real_name"
                placeholder="실명"
                required
              />
              <label for="real-name">실명</label>
            </div>
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="registerForm.username"
                placeholder="사용할 계정명 (ID)"
                pattern="^.{1,65}$"
                required
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="최대 64자에, 한글을 비롯하여 어떤 문자든 허용됩니다."
              />
              <label for="username">사용할 계정명 (ID)</label>
            </div>
            <div class="form-floating">
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="registerForm.password"
                placeholder="사용할 비밀번호"
                pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="10자 이상에 숫자와 영문이 하나씩은 있어야 합니다."
                required
              />
              <label for="password">사용할 비밀번호</label>
            </div>
            <div class="form-floating">
              <input
                type="password"
                class="form-control"
                id="password-confirm"
                placeholder="사용할 비밀번호 재입력"
                v-model="registerForm.passwordConfirm"
                required
              />
              <label for="password-confirm">사용할 비밀번호 재입력</label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button class="btn btn-light" data-bs-dismiss="modal" @click="submit">
            가입
          </button>
        </div>
      </div>
    </div>
  </div>
  <nav class="navbar navbar-expand-lg fixed-top">
    <div class="container-fluid" id="navbar-header">
      <div id="dummy" tableindex="-1"></div>
      <RouterLink class="navbar-brand" to="/">연세문학회</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasNavbar"
        aria-controls="offcanvasNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        id="offcanvasNavbar"
        aria-labelledby="offcanvasNavbarLabel"
      >
        <div class="offcanvas-header">
          <h3 class="offcanvas-title hanja" id="offcanvasNavbarLabel">
            연세문학회
          </h3>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/about"
                ><span data-bs-dismiss="offcanvas">소개 About</span></RouterLink
              >
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link active dropdown-toggle"
                id="offcanvasNavbarDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                분반 Class
              </a>
              <ul
                class="dropdown-menu"
                aria-labelledby="offcanvasNavbarDropdown"
              >
                <RouterLink
                  v-for="c in classes"
                  class="dropdown-item"
                  :key="c"
                  :to="'/classes/' + c.name"
                  ><span data-bs-dismiss="offcanvas">{{
                    c.korean
                  }}</span></RouterLink
                >
              </ul>
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/magazines"
                ><span data-bs-dismiss="offcanvas"
                  >문집 Magazine</span
                ></RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/notices"
                ><span data-bs-dismiss="offcanvas"
                  >공지 Notice</span
                ></RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/rules"
                ><span data-bs-dismiss="offcanvas">회칙 Rules</span></RouterLink
              >
            </li>
            <li class="nav-item" v-if="!store.isAuthenticated">
              <a
                class="nav-link active"
                data-bs-toggle="modal"
                href="#login-modal"
                role="button"
                >접속 Login</a
              >
            </li>
            <li class="nav-item" v-else>
              <RouterLink
                to="/logout"
                class="nav-link active"
                aria-current="page"
                >접속해제 Logout</RouterLink
              >
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link active dropdown-toggle"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                가입 Join
              </a>
              <ul
                class="dropdown-menu"
                aria-labelledby="offcanvasNavbarDropdown"
              >
                <a :href="joinFormUrl" class="dropdown-item">동아리 가입</a>
                <a
                  data-bs-toggle="modal"
                  href="#register-modal"
                  role="button"
                  class="dropdown-item"
                  >사이트 가입</a
                >
              </ul>
            </li>
            <li class="nav-item" v-if="store.isAuthenticated">
              <RouterLink class="nav-link active" aria-current="page" to="/me"
                ><span data-bs-dismiss="offcanvas"
                  >내 정보 Profile</span
                ></RouterLink
              >
            </li>
            <li class="nav-item" v-if="store.isAdmin">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/admin"
                ><span data-bs-dismiss="offcanvas"
                  >관리 Manage</span
                ></RouterLink
              >
            </li>
          </ul>
          <!-- <form class="d-flex" role="search">
            <input
              class="form-control me-2"
              type="search"
              placeholder="검색"
              aria-label="Search"
            />
            <button class="btn btn-outline-success" type="submit">검색</button>
          </form> -->
        </div>
      </div>
    </div>
  </nav>
</template>

<style>
@media (max-width: 991px) {
  .navbar-brand {
    position: absolute;
    left: 50%;
    transform: translate(-50%, 0);
  }
}
.contact-icon {
  margin-right: 3px;
}
#offcanvasNavbar {
  max-width: 75%;
}
nav,
.offcanvas-header,
.offcanvas-body {
  background-color: #ffdddd;
}
.navbar {
  box-shadow: 0 3px 5px rgb(57 63 72 / 30%);
}
.nav-link {
  color: #564138 !important;
}
</style>
