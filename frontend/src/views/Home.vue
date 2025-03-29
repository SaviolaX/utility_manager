<template>
  <div>
    <h1>Welcome to HOME page!!</h1>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { getCurrentUser } from "aws-amplify/auth";

export default {
  name: "Home",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    return { authStore, router };
  },
  async mounted() {
    try {
      const user = await getCurrentUser();
      if (user) {
        this.authStore.setUser(
          {
            username: user.username,
            email: user.signInDetails?.loginId,
          },
          {
            isLoggedIn: true,
          }
        );
        console.log(`Home: user ${user.username} logged in.`);
      }
    } catch (err) {
      console.log("No user on mounted in Home.");
    }
  },
};
</script>

<style>
</style>
