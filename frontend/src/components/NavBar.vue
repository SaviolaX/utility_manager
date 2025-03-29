<template>
  <nav class="nav-wrapper">
    <div class="nav-title">
      <router-link class="nav-title-link" to="/"
        ><h2>App title</h2></router-link
      >
    </div>
    <div class="nav-auth">
      <p v-if="authStore.user">Current user, {{ user.email }}</p>
      <button v-if="authStore.user" @click="signOutUser">Logout</button>
      <router-link v-if="!authStore.user" to="/signin">Login</router-link>
      <router-link v-if="!authStore.user" to="/signup">Register</router-link>
    </div>
  </nav>
</template>

<script>
import { signOut } from "aws-amplify/auth";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { computed } from "vue";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const user = computed(() => authStore.user);

    const signOutUser = async () => {
      try {
        await signOut();
        authStore.clearUser();
        router.push("/signin");
      } catch (err) {
        console.error("Sign-out error: ", err);
      }
    };

    return { authStore, signOutUser, user };
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
        console.log(`User ${user.username} logged in.`);
      }
    } catch (err) {
      console.log("No user on mounted NavBar.");
    }
  },
};
</script>

<style>
.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #333;
  color: white;
  box-sizing: border-box;
}
.nav-auth {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nav-auth a {
  color: white;
  margin-left: 10px;
  text-decoration: none;
}
.nav-auth a:hover {
  text-decoration: underline;
}
.nav-title-link {
  text-decoration: none;
  color: aliceblue;
}
</style>