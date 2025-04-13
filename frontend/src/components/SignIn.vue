<template>
  <div class="signin-container">
    <h2>Login</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="signInUser">Sign In</button>
    <p>
      If you don't have an account,
      <router-link to="/signup">Register</router-link>.
    </p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>
  
<script>
import { signIn, getCurrentUser } from "aws-amplify/auth";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

export default {
  setup() {
    const router = useRouter();

    const email = ref("");
    const password = ref("");
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
          console.log("From SignIn: User is not authenticated.");
        } else {
          console.error("Unexpected error: ", err);
        }
      }
    });

    const signInUser = async () => {
      const loginPayload = {
        username: email.value, // method signIn accepts email as username. Configured in cognito.
        password: password.value,
      };
      try {
        await signIn(loginPayload);
        error.value = null;

        console.log("Logged in successfully.");
        router.push("/"); // Redirect to home or dashboard
      } catch (err) {
        error.value = err.message;
        if (err.name === "UserNotFoundException") {
          console.error("Sign-in error:", err.message);
        } else {
          console.log("Unexpected error: ", err);
        }
      }
    };

    return { email, password, error, signInUser };
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