<script setup>
import { useMemberStore } from "../stores/member";
import axios from "axios";
import LoginModal from "./LoginModal.vue";
import RegisterModal from "./RegisterModal.vue";
</script>
<script>
export default {
  data() {
    return {
      store: useMemberStore(),
      classes: [],
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
    logout() {
      this.store.logOut();
      this.$router.replace("/");
    },
  },
};
</script>
<template>
  <LoginModal id="login-modal"></LoginModal>
  <RegisterModal id="register-modal"></RegisterModal>
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
              <a role="button" class="nav-link active" @click="logout"
                >접속해제 Logout</a
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
@media (max-width: 334px) {
  #offcanvasNavbar {
    max-width: 65%;
  }
}
@media only screen and (min-width: 335px) and (max-width: 991px) {
  #offcanvasNavbar {
    max-width: 50%;
  }
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
