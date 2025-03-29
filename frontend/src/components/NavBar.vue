<template>
  <nav class="nav-wrapper">
    <div class="nav-title">
      <router-link class="nav-title-link" to="/"
        ><h2>App title</h2></router-link
      >
    </div>
    <div class="nav-auth">
      <p v-if="authStore.user">{{ user.email }}</p>
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
/* Navigation wrapper */
.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #E5E7EB; /* Pure white for a clean look */
  color: #374151; /* Dark gray text */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  box-sizing: border-box;
}
/* Title section */
.nav-title {
  display: flex;
  align-items: center;
}
/* Title text */
.nav-title h2 {
  margin: 15px;
  font-size: 24px; /* Larger font size for title */
  color: #374151; /* Soft blue for title */
  font-weight: 600; /* Slightly bolder for emphasis */
}

/* Authentication section */
.nav-auth {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Links in the auth section */
.nav-auth a {
  color: white; /* Medium gray for links */
  margin-left: 10px;
  text-decoration: none;
  transition: color 0.3s ease; /* Smooth hover transition */
}

/* Hover effect for auth links */
.nav-auth a:hover {
  color: #60A5FA; /* Soft blue for hover */
  text-decoration: underline;
}

/* Button in auth section */
.nav-auth button {
  background-color: #3B82F6; /* Clean blue for button */
  color: #FFFFFF; /* White text */
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease; /* Smooth hover transition */
}

/* Hover effect for button */
.nav-auth button:hover {
  background-color: #2563EB; /* Darker blue for hover */
}

/* Paragraph in auth section */
.nav-auth p {
  margin: 0 10px;
  font-size: 18px;
  font-weight: 500; /* Medium weight for text */
  color: #374151; /* Dark gray for text */
}

/* Title link */
.nav-title-link {
  text-decoration: none;
  color: #374151; /* Dark gray for title */
  font-weight: 600; /* Slightly bolder for emphasis */
  transition: color 0.3s ease; /* Smooth hover transition */
}

/* Hover effect for title link */
.nav-title-link:hover {
  color: #60A5FA; /* Soft blue for hover */
}
</style>