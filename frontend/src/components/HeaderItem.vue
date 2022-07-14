<script setup>
import { useMemberStore } from "../stores/member";
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
                href="#"
                class="nav-link active"
                aria-current="page"
                data-bs-toggle="collapse"
                data-bs-target="#loginForm"
                >인증 Login</a
              >
            </li>
            <li class="nav-item" v-else>
              <RouterLink
                to="/logout"
                class="nav-link active"
                aria-current="page"
                >인증해제 Logout</RouterLink
              >
            </li>
            <li class="collapse" id="loginForm">
              <form @submit.prevent="submit">
                <div class="mb-3">
                  <input
                    type="text"
                    class="form-control"
                    id="exampleInputEmail1"
                    aria-describedby="emailHelp"
                    placeholder="계정명 ID"
                    required
                    v-model="loginForm.username"
                  />
                  <small>계정명을 모르신다면</small>
                  <input
                    type="password"
                    class="form-control"
                    id="exampleInputPassword1"
                    placeholder="비밀번호 Password"
                    required
                    v-model="loginForm.password"
                  />
                  <small>비밀번호를 모르신다면</small>
                  <div id="emailHelp" class="form-text">
                    <button type="submit" class="btn btn-primary">접속</button>
                  </div>
                </div>
              </form>
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
                    href="#"
                    data-bs-toggle="collapse"
                    data-bs-target="#registerForm"
                    >사이트 가입</a
                  >
                </li>
              </ul>
            </li>
            <li class="collapse" id="registerForm">
              <form @submit.prevent="submit">
                <div class="mb-3">
                  <input
                    type="number"
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
                    aria-describedby="portalPWHelp"
                    required
                  />
                  <small id="portalPWHelp"
                    >연세포탈 비밀번호는 신촌캠 구성원 인증에만 일회용되고, 인증
                    즉시 폐기됩니다. <i>연세문학회를 믿으세요.</i></small
                  >
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
                    placeholder="사용할 계정명"
                    pattern="^.{1,65}$"
                    required
                    aria-describedby="IDHelp"
                  />
                  <small id="IDHelp">
                    계정명은 최대 64자에, <u>한글을 비롯하여 어떤 문자든</u>
                    허용됩니다.
                  </small>
                  <input
                    type="password"
                    class="form-control"
                    v-model="registerForm.password"
                    placeholder="사용할 비밀번호"
                    aria-describedby="PWHelp"
                    pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
                    required
                  />
                  <input
                    type="password"
                    class="form-control"
                    v-model="registerForm.password"
                    placeholder="사용할 비밀번호 재입력"
                    pattern="^(?=.*[0-9])(?=.*[a-zA-Z]).{10,}$"
                    required
                  />
                  <small id="PWHelp">
                    비밀번호는 10자 이상에 숫자와 영문이 하나씩은 있어야 합니다.
                  </small>
                </div>
              </form>
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
              <p>📌 {{ address }}</p>
              <p>
                📧 <a :href="'mailto:' + email">{{ email }}</a>
              </p>
              <p>
                📞 회장 {{ presidentName }}
                <a :href="'tel:' + presidentTel">{{ presidentTel }}</a>
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
                    src="Github-Mark-32px.png"
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
header {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
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
</style>
