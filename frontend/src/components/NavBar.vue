<template>
  <nav class="nav-wrapper">
    <div class="nav-title">
      <router-link class="nav-title-link" to="/"
        ><h2>App title</h2></router-link
      >
    </div>
    <div v-if="authStore.isLoggedIn" class="nav-auth">
      <p>{{ authStore.user.email }}</p>
      <button @click="signOutUser">Logout</button>
    </div>
    <div v-if="!authStore.isLoggedIn" class="nav-auth">
      <router-link to="/signin">Login</router-link>
      <router-link to="/signup">Register</router-link>
    </div>
  </nav>
</template>

<script>
import { signOut, getCurrentUser } from "aws-amplify/auth";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const signOutUser = async () => {
      try {
        await signOut();
        authStore.clearUser();
        router.push("/signin");
      } catch (err) {
        console.error("Sign-out error: ", err);
      }
    };

    return { authStore, signOutUser };
  },
  async mounted() {
    const user = await getCurrentUser();
    if (user) {
      this.authStore.setUser({
        user: {
          email: user.signInDetails.loginId,
          username: user.username,
        },
        isLoggedIn: true,
      });
    } else {
      console.log("No user logged in.");
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
  background-color: #374151; /* Dark Theme: Medium-dark gray, matching other blocks */
  color: #d1d5db; /* Dark Theme: Default light gray text */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow */
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
  font-size: 24px;
  color: #f9fafb; /* Dark Theme: Brighter white/light gray for title */
  font-weight: 600;
}

/* Authentication section */
.nav-auth {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Links in the auth section */
.nav-auth a {
  /* Note: Original CSS had 'color: white;' on a light gray bg, which seems incorrect.
     Assuming it should have been dark text, now making it light. */
  color: #d1d5db; /* Dark Theme: Light gray for links */
  margin-left: 10px;
  text-decoration: none;
  transition: color 0.3s ease;
}

/* Hover effect for auth links */
.nav-auth a:hover {
  color: #60a5fa; /* Soft blue for hover - should stand out */
  text-decoration: underline;
}

/* Button in auth section */
.nav-auth button {
  background-color: #3b82f6; /* Keeping blue button */
  color: #ffffff; /* White text */
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* Hover effect for button */
.nav-auth button:hover {
  background-color: #2563eb; /* Darker blue for hover */
}

/* Paragraph in auth section */
.nav-auth p {
  margin: 0 10px;
  font-size: 18px;
  font-weight: 500;
  color: #d1d5db; /* Dark Theme: Light gray for text */
}

/* Title link */
.nav-title-link {
  text-decoration: none;
  color: #f9fafb; /* Dark Theme: Brighter white/light gray, matching h2 */
  font-weight: 600;
  transition: color 0.3s ease;
}

/* Hover effect for title link */
.nav-title-link:hover {
  color: #60a5fa; /* Soft blue for hover */
}
</style>