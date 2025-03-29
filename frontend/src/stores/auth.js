import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    isLoggedIn: false,
  }),
  actions: {
    setUser(userData, isLoggedIn) {
      this.user = userData;
      this.isLoggedIn = isLoggedIn;
    },
    clearUser() {
      this.user = null;
      this.isLoggedIn = false;
    },
  },
});
