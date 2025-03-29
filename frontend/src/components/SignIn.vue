<template>
  <div class="signin-container">
    <h2>Login</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="signInUser">Sign In</button>
    <p>If you don't have an account, <router-link to="/signup">Register</router-link>.</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>
  
<script>
import { signIn, getCurrentUser } from "aws-amplify/auth";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    return { authStore, router };
  },
  data() {
    return {
      email: "",
      password: "",
      error: null,
    };
  },
  async mounted() {
    try {
      const user = await getCurrentUser();
      if (user) {
        console.log("User is authenticated. Redirect to Home page.");
        this.router.push("/");
      }
    } catch (err) {
      console.log("No user on mounted in SignIn");
    }
  },
  methods: {
    async signInUser() {
      const loginPayload = {
        username: this.email, // method signIn accepts email as username. Configured in cognito.
        password: this.password,
      };
      try {
        await signIn(loginPayload);
        this.error = null;

        const user = await getCurrentUser();
        // Set user data in the store
        this.authStore.setUser(
          {
            username: user.username,
            email: user.signInDetails?.loginId,
          },
          {
            isLoggedIn: true,
          }
        );
        this.router.push("/"); // Redirect to home or dashboard
      } catch (err) {
        this.error = err.message;
        console.error("Sign-in error:", err);
      }
    },
  },
};
</script>
<style>
.signin-container {
  text-align: center;
  margin-top: 50px;
}
.signin-container a {
  color: #ebdbb2; /* Gruvbox light beige for links */
  text-decoration: none;
  font-weight: bold;
  font-size: 18px;
  transition: color 0.3s ease; /* Smooth hover transition */
}
.signin-container input {
  display: block;
  margin: 10px auto;
  padding: 10px;
  width: 200px;
}
.signin-container button {
  margin: 10px auto;
  padding: 10px;
  width: 100px;
}
.signin-container h2 {
  color: white;
  font-size: 2em;
}
.signin-container p {
  color: white;
}
</style>