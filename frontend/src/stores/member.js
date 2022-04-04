import { defineStore } from "pinia";
import axios from "axios";

export const useMemberStore = defineStore({
  id: "member",
  state: () => ({
    member: null,
    token: "",
    tokenType: "",
  }),
  getters: {
    isAuthenticated: (state) => state.member !== null,
    stateMember: (state) => state.member,
    isAdmin: (state) =>
      state.isAuthenticated && state.member.role in ["board", "president"],
    authorizationHeader: (state) => state.tokenType + " " + state.token,
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
    whoAmI() {
      axios
        .get("/me", {
          headers: {
            Authorization: this.authorizationHeader,
          },
        })
        .then((response) => {
          this.member = {
            username: response.data.username,
            realName: response.data.real_name,
            studentId: response.data.student_id,
            role: response.data.role,
          };
        })
        .catch((error) => {
          console.error(error);
        });
      return this.member;
    },
    logOut() {
      this.member = null;
      this.token = "";
      this.tokenType = "";
    },
  },
});
