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
      footer: {
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
      this.footer.address = res.data.address;
      this.footer.email = res.data.email;
      this.footer.presidentName = res.data.president_name;
      this.footer.presidentTel = res.data.president_tel;
      this.footer.joinFormUrl = res.data.joinFormUrl;
    } catch (error) {
      console.log(error);
    }
  },
};
</script>

<template>
  <HeaderItem></HeaderItem>
  <RouterView :key="$route.path" />
  <FooterItem v-bind="footer"></FooterItem>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Serif+KR:wght@200;600&display=swap");
@import "@/assets/base.css";
* {
  font-family: inherit;
}
#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;

  font-weight: normal;
  font-family: "Gowun Batang", serif;
  background: #ffdddd;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  body {
    display: flex;
    place-items: center;
  }

  #app {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 2rem;
  }

  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
.active {
  background-color: pink;
  border-color: pink;
}
</style>
