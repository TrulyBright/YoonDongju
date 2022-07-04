<script setup>
import { useMemberStore } from "../stores/member";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      openLoginModal: false,
      store: useMemberStore(),
      classes: [],
      form: {
        username: null,
        password: null,
      },
    };
  },
  async created() {
    const response = await axios.get("classes");
    this.classes = response.data;
  },
  methods: {
    async submit() {
      const store = useMemberStore();
      await store.requestToken(this.form);
      await store.whoAmI();
    },
  },
};
</script>
<template>
  <header>
    <BButton to="/">연세문학회</BButton>
    <BButton to="/about">소개</BButton>
    <BDropdown text="분반">
      <BDropdownItem v-for="c in classes" :key="c" :to="'/classes/' + c.name">{{
        c.korean
      }}</BDropdownItem>
    </BDropdown>
    <BButton to="/magazines">문집</BButton>
    <BButton to="/notices">공지</BButton>
    <BButton to="/admin" v-if="store.isAdmin">관리</BButton>
    <BButton to="/me" v-if="store.isAuthenticated">내정보</BButton>
    <!-- Button trigger modal -->
    <button
      type="button"
      class="btn btn-primary"
      data-bs-toggle="modal"
      data-bs-target="#exampleModal"
      @click="openLoginModal = true"
      v-if="!store.isAuthenticated"
    >
      로그인
    </button>
    <!-- Modal -->
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="submit">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLabel">로그인</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">ID</label>
                <input
                  type="text"
                  class="form-control"
                  id="exampleInputEmail1"
                  aria-describedby="emailHelp"
                  placeholder="ID"
                  required
                  v-model="form.username"
                />
                <div id="emailHelp" class="form-text">
                  한글을 비롯하여 어떤 문자든 허용됩니다. ID를 모르시나요?
                </div>
              </div>
              <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label"
                  >비밀번호</label
                >
                <input
                  type="password"
                  class="form-control"
                  id="exampleInputPassword1"
                  placeholder="비밀번호"
                  required
                  v-model="form.password"
                />
                <div id="emailHelp" class="form-text">
                  10자 이상에 숫자와 영문이 하나씩은 있어야 합니다. 비밀번호를
                  모르시나요?
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                닫기
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                data-bs-dismiss="modal"
              >
                접속
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <Teleport to="#app">
      <LoginModal
        v-if="openLoginModal"
        @close="openLoginModal = false"
      ></LoginModal>
    </Teleport>
    <RouterLink to="/" @click="store.logOut" v-if="store.isAuthenticated"
      >로그아웃</RouterLink
    >
  </header>
</template>

<style>
header {
  display: flex;
  flex-direction: row;
  gap: 15px;
}
</style>
