<template>
  <div class="confirm-signup-container">
    <h2>Confirm Sign Up</h2>
    <p>Please enter the confirmation code sent to your email.</p>
    <input v-model="code" placeholder="Confirmation Code" />
    <button @click="confirmSignUpUser">Confirm</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>
  
  <script>
import { confirmSignUp } from "aws-amplify/auth";
import { getCurrentUser } from "aws-amplify/auth";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { onMounted } from "vue";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const route = useRoute();

    onMounted(async () => {
      const userId = route.query.userId;
      if (!userId) {
        console.warn("No userId in query params. Redirecting...");
        router.push("/");
      }

      try {
        const user = await getCurrentUser();

        if (user) {
          console.log("User is authenticated. Redirecting to Home page.");
          router.push("/");
        }
      } catch (err) {
        console.log("User needs to confirm their signup. Stay on the page.");
        console.error("No user on mounted in ConfirmPage.");
      }
    });
    return { authStore, router, route };
  },
  data() {
    return {
      username: "",
      code: "",
      error: null,
    };
  },

  methods: {
    async confirmSignUpUser() {
      try {
        this.username = this.$route.query.userId;
        const confirmSignUpPayload = {
          username: this.username,
          confirmationCode: this.code,
        };
        const createdUser = await confirmSignUp(confirmSignUpPayload);
        console.log("Created user from confirm page: ", createdUser);
        this.router.push("/signin"); // Redirect to login after confirmation
      } catch (err) {
        this.error = err.message;
      }
    },
  },
};
</script>
<style>
.confirm-signup-container {
  text-align: center;
  margin-top: 50px;
}
.confirm-signup-container input {
  margin: 10px;
  padding: 5px;
}
.confirm-signup-container button {
  padding: 5px 10px;
  border: none;
  cursor: pointer;
}
.confirm-signup-container p {
  color: white;
}
.confirm-signup-container h2 {
  color: white;
}
</style>