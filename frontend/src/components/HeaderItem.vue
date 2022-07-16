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
    const tooltipList = [...tooltipTriggerList].map(
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
            <div class="mb-3">
              <input
                type="text"
                class="form-control"
                placeholder="계정명 ID"
                required
                v-model="loginForm.username"
              />
              <input
                type="password"
                class="form-control"
                placeholder="비밀번호 Password"
                required
                v-model="loginForm.password"
              />
              <button type="submit" class="btn btn-primary">접속</button>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-primary"
            data-bs-target="#forgot-id-pw"
            data-bs-toggle="modal"
            data-bs-dismiss="modal"
          >
            계정명을 모르시나요?
          </button>
          <button
            class="btn btn-primary"
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
            class="btn btn-primary"
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
            <div class="mb-3">
              <input
                type="text"
                class="form-control"
                v-model="registerForm.portal_id"
                placeholder="연세포탈 ID"
                required
              />
              <input
                type="password"
                class="form-control"
                v-model="registerForm.portal_pw"
                placeholder="연세포탈 비밀번호"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="저장되지 않고, 신촌캠 구성원 확인에만 일회용됩니다."
                required
              />
              <input
                type="text"
                class="form-control"
                v-model="registerForm.real_name"
                placeholder="실명"
                required
              />
              <input
                type="text"
                class="form-control"
                v-model="registerForm.username"
                placeholder="사용할 계정명 (ID)"
                pattern="^.{1,65}$"
                required
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="최대 64자에, 한글을 비롯하여 어떤 문자든 허용됩니다."
              />
              <input
                type="password"
                class="form-control"
                v-model="registerForm.password"
                placeholder="사용할 비밀번호"
                pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                title="10자 이상에 숫자와 영문이 하나씩은 있어야 합니다."
                required
              />
              <input
                type="password"
                class="form-control"
                placeholder="사용할 비밀번호 재입력"
                v-model="registerForm.passwordConfirm"
                required
              />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="submit"
          >
            가입
          </button>
        </div>
      </div>
    </div>
  </div>
  <nav class="navbar navbar-expand-lg bg-light fixed-top">
    <div class="container-fluid" id="navbar-header">
      <RouterLink class="navbar-brand" id="navbar-brand" to="/"
        >연세문학회</RouterLink
      >
      <button
        class="navbar-toggler"
        id="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasNavbar"
        aria-controls="offcanvasNavbar"
      >
        <i class="bi-three-dots"></i>
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
                >소개 About</RouterLink
              >
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
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
                <li v-for="c in classes" class="dropdown-item" :key="c">
                  <RouterLink :to="'/classes/' + c.name">{{
                    c.korean
                  }}</RouterLink>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/magazines"
                >문집 Magazine</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/notices"
                >공지 Notice</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/rules"
                >회칙 Rules</RouterLink
              >
            </li>
            <li class="nav-item" v-if="!store.isAuthenticated">
              <a
                class="nav-link"
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
                class="nav-link dropdown-toggle"
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
                <li class="dropdown-item">
                  <a :href="joinFormUrl">동아리 가입</a>
                </li>
                <li class="dropdown-item">
                  <a
                    
                data-bs-toggle="modal"
                href="#register-modal"
                role="button"
                    >사이트 가입</a
                  >
                </li>
              </ul>
            </li>
            <li class="nav-item" v-if="store.isAuthenticated">
              <RouterLink class="nav-link active" aria-current="page" to="/me"
                >내 정보 Profile</RouterLink
              >
            </li>
            <li class="nav-item" v-if="store.isAdmin">
              <RouterLink
                class="nav-link active"
                aria-current="page"
                to="/admin"
                >관리 Manage</RouterLink
              >
            </li>
          </ul>
          <div class="mobile-info">
            <div>
              <h5>연락처</h5>
              <p><span class="contact-icon">📌</span>{{ address }}</p>
              <p>
                <span class="contact-icon">📧</span
                ><a :href="'mailto:' + email">{{ email }}</a>
              </p>
              <p>
                <span class="contact-icon">📞</span>회장 {{ presidentName }}
                <a :href="'tel:' + presidentTel">{{ presidentTel }}</a>
              </p>
              <p>
                <span class="contact-icon">💻</span>개발자
                <a href="mailto:trulybright@yonsei.ac.kr"
                  >trulybright@yonsei.ac.kr</a
                >
              </p>
            </div>
            <div>
              <h5>서체</h5>
              <p>
                한글/영문:
                <a
                  href="https://fonts.google.com/specimen/Gowun+Batang?subset=korean"
                  >고운 바탕</a
                >
              </p>
              <p>
                한자:
                <a
                  href="https://fonts.google.com/noto/specimen/Noto+Serif+KR?subset=korean"
                  >Noto Serif Korean</a
                >
              </p>
            </div>
            <div>
              <h5>사이트 정보</h5>
              <p>
                <a href="https://github.com/TrulyBright/YoonDong-ju"
                  ><img
                    src="@/assets/Github-Mark-32px.png"
                    alt="깃허브 아이콘. 클릭하면 깃허브의 연세문학회 프로젝트 레포지토리로 이동함."
                /></a>
              </p>
            </div>
          </div>
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
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css");
@media (min-width: 992px) {
  /* 992px: lg */
  .mobile-info {
    display: none;
  }
}
@media (max-width: 991px) {
  #navbar-header {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
  #navbar-toggler {
    position: absolute;
    right: 0;
  }
  #navbar-brand {
    margin-right: unset;
  }
}
.contact-icon {
  margin-right: 3px;
}
</style>
