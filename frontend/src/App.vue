<template>
  <NavBar />

  <div class="content-wrapper">
    <h1>Welcome to Vue</h1>
    <div v-if="response">
      {{ response }}
    </div>
    <p v-else>No data...</p>
    <button @click="fetchData">Fetch Data</button>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";

const HELLO_ENDPOINT =
  "https://46k9mn6ytl.execute-api.eu-central-1.amazonaws.com/dev/hello";

const TEST_ENDPOINT = "https://jsonplaceholder.typicode.com/todos/1";

export default {
  name: "App",
  components: {
    NavBar,
  },

  data() {
    return {
      response: null,
    };
  },

  methods: {
    async fetchData() {
      const response = await fetch(HELLO_ENDPOINT, {
        method: "GET",
      });
      const data = await response.json();
      console.log(data);
      this.response = data;
    },
  },
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
