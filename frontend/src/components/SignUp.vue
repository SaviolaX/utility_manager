<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <input
      v-model="confirm_password"
      type="password"
      placeholder="Confirm password"
    />
    <button @click="signUpUser">Sign Up</button>
    <p>
      If you already have an account,
      <router-link to="/signin">Sign in</router-link>.
    </p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>
  
  <script>
import { signUp } from "aws-amplify/auth";
import { useRouter } from "vue-router";
import { getCurrentUser } from "aws-amplify/auth";
import { ref, onMounted } from "vue";

export default {
  setup() {
    const router = useRouter();

    const email = ref("");
    const password = ref("");
    const confirm_password = ref("");
    const error = ref(null);

    onMounted(async () => {
      try {
        const user = await getCurrentUser();
        if (user) {
          console.log("User is authenticated. Redirect to Home page.");
          router.push("/");
        }
      } catch (err) {
        if (err.name === "UserUnAuthenticatedException") {
          console.log("From SignUp: User is not authenticated.");
        } else {
          console.error("Unexpected error: ", err);
        }
      }
    });

    const signUpUser = async () => {
      const signUpPayload = {
        username: email.value, // method signUp accepts email as username. Configured in cognito.
        password: password.value,
      };
      try {
        const user = await signUp(signUpPayload);
        error.value = null;
        // After sign-up, user needs to confirm (e.g., via email code)
        router.push({
          path: "/confirm-signup",
          query: { userId: user.userId },
        }); // Redirect to confirmation page with userId
      } catch (err) {
        error.value = err.message;
        console.error("Sign-up error:", err);
      }
    };

    return {
      signUpUser,
      email,
      password,
      confirm_password,
      error,
    };
  },
};
</script>
<style>
.signup-container {
  text-align: center;
  margin-top: 50px;
}
.signup-container a {
  color: #ebdbb2; /* Gruvbox light beige for links */
  text-decoration: none;
  font-weight: bold;
  font-size: 18px;
  transition: color 0.3s ease; /* Smooth hover transition */
}
.signup-container input {
  display: block;
  margin: 10px auto;
  padding: 10px;
  width: 200px;
}
.signup-container button {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}
.signup-container h2 {
  color: white;
  font-size: 2em;
}
.signup-container p {
  color: white;
}
</style>