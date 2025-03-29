<template>
  <div>
    <h2>Login</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="signInUser">Sign In</button>
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