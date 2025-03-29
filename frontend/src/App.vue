<template>
  <div>
    <NavBar />
    <router-view />
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import "@aws-amplify/ui-vue/styles.css";

export default {
  name: "App",
  components: {
    NavBar,
  },

  setup() {},
};
</script>

<style>
body,
html {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #585858;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.content-wrapper {
  padding: 20px;
  color: white;
  text-align: center;
}
.content-wrapper h1 {
  font-size: 2em;
  margin-bottom: 20px;
}
</style>
