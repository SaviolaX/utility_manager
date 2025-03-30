import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isLoggedIn: false,
    authToken: null,
  }),
  actions: {
    setUser({ user, isLoggedIn, authToken }) {
      // Destructured object parameter
      this.user = user;
      this.isLoggedIn = isLoggedIn;
      this.authToken = authToken;
    },
    clearUser() {
      this.user = null;
      this.isLoggedIn = false;
      this.authToken = null;
    },
  },
});
