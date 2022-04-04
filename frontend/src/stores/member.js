import { defineStore } from "pinia";
import axios from "axios";

export const useMemberStore = defineStore({
  id: "member",
  state: () => ({
    member: null,
    token: null,
    tokenType: null,
  }),
  getters: {
    isAuthenticated: (state) => state.member !== null,
    stateMember: (state) => state.member,
    isAdmin: (state) =>
      state.isAuthenticated && state.member.role in ["board", "president"],
  },
  actions: {
    async register(form) {
      const response = await axios.post("/register", form);
      this.member = {
        username: response.data.username,
        realName: response.data.real_name,
        studentId: response.data.student_id,
        role: response.data.role,
      };
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
    },
    async whoAmI() {
      const response = await axios.get("/me", {
        headers: {
          Authorization: this.tokenType + " " + this.token,
        }
      });
      this.member = {
        username: response.data.username,
        realName: response.data.real_name,
        studentId: response.data.student_id,
        role: response.data.role,
      };
    },
    async logOut() {
      this.member = null;
    },
  },
});
