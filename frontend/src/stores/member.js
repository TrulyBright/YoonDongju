import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";

export const useMemberStore = defineStore({
  id: "member",
  state: () => ({
    member: useLocalStorage("member", ""),
    token: useLocalStorage("token", ""),
    tokenType: useLocalStorage("tokenType", ""),
    expiresAt: useLocalStorage("expiresAt", ""),
  }),
  getters: {
    isAuthenticated: (state) =>
      state.member !== "" && Date.now() / 1000 < state.expiresAt,
    stateMember: (state) => JSON.parse(state.member),
    isAdmin: (state) =>
      state.isAuthenticated &&
      (state.stateMember.role === "board" ||
        state.stateMember.role === "president"),
    authorizationHeader: function (state) {
      // why not arrow lambda?: to use "this".
      return state.tokenType + " " + state.token;
    },
  },
  actions: {
    async register(form) {
      const response = await axios.post("/register", form);
      this.member = JSON.stringify({
        username: response.data.username,
        realName: response.data.real_name,
        studentId: response.data.student_id,
        role: response.data.role,
      });
      await this.requestToken({
        username: form.username,
        password: form.password,
      });
    },
    async requestToken(idPw) {
      const data = new FormData();
      data.append("username", idPw.username);
      data.append("password", idPw.password);
      const result = await axios.post("/token", data);
      this.token = result.data.access_token;
      this.tokenType = result.data.token_type;
      this.expiresAt = result.data.expires_at;
    },
    async whoAmI() {
      const response = await axios.get("/me", {
        headers: {
          Authorization: this.authorizationHeader,
        },
      });
      this.member = JSON.stringify({
        username: response.data.username,
        realName: response.data.real_name,
        studentId: response.data.student_id,
        role: response.data.role,
      });
      return this.stateMember;
    },
    logOut() {
      this.member = "";
      this.token = "";
      this.tokenType = "";
    },
  },
});
