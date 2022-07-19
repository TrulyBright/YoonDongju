<script setup>
import { RouterView } from "vue-router";
import HeaderItem from "@/components/HeaderItem.vue";
import FooterItem from "@/components/FooterItem.vue";
import axios from "axios";
</script>
<script>
export default {
  data() {
    return {
      contacts: {
        address: "주소가 없음",
        email: "메일이 없음",
        presidentName: "회장 이름이 없음",
        presidentTel: "회장 전화번호가 없음",
        joinFormUrl: "가입 주소가 없음",
      },
    };
  },
  async created() {
    try {
      const res = await axios.get("/club-information");
      this.contacts.address = res.data.address;
      this.contacts.email = res.data.email;
      this.contacts.presidentName = res.data.president_name;
      this.contacts.presidentTel = res.data.president_tel;
      this.contacts.joinFormUrl = res.data.joinFormUrl;
    } catch (error) {
      console.log(error);
    }
  },
};
</script>

<template>
  <HeaderItem v-bind="contacts"></HeaderItem>
  <div id="main">
    <RouterView :key="$route.path" />
  </div>
  <FooterItem v-bind="contacts" id="footer"></FooterItem>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Serif+KR:wght@200;600&display=swap");
@import "@/assets/base.css";
* {
  font-family: inherit;
  color: #564138;
}
#app {
  margin: 0 auto;

  font-weight: normal;
  font-family: "Gowun Batang", serif;
  background: #ffdddd;
}
.hanja {
  font-family: "Noto Serif KR", serif;
}
a:link {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
button.btn.btn-pink {
  background-color: #ffdddd;
}
#main {
  padding: 1.5em;
  padding-top: 5em;
}
@media (min-width: 992px) {
  #main {
    padding-left: 20%;
    padding-right: 20%;
  }
}
#footer {
  background: white;
}
</style>
