<template>
  <div>
    <h2>Sign Up</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <input
      v-model="confirm_password"
      type="password"
      placeholder="Confirm password"
    />
    <button @click="signUpUser">Sign Up</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>
  
  <script>
import { signUp } from "aws-amplify/auth";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { getCurrentUser } from "aws-amplify/auth";

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
      confirm_password: "",
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
      console.log("No user on mounted in SignUp.");
    }
  },
  methods: {
    async signUpUser() {
      const signUpPayload = {
        username: this.email, // method signUp accepts email as username. Configured in cognito.
        password: this.password,
      };
      try {
        const user = await signUp(signUpPayload);
        this.error = null;
        // After sign-up, user needs to confirm (e.g., via email code)
        this.router.push({
          path: "/confirm-signup",
          query: { userId: user.userId },
        }); // Redirect to confirmation page with userId
      } catch (err) {
        this.error = err.message;
        console.error("Sign-up error:", err);
      }
    },
  },
};
</script>