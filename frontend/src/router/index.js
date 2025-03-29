import { createRouter, createWebHistory } from "vue-router";
import SignIn from "@/components/SignIn.vue";
import SignUp from "@/components/SignUp.vue";
import ConfirmSingUp from "@/components/ConfirmSingUp.vue";
import Home from "@/views/Home.vue";
import Error404 from "@/components/Error404.vue";

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/signin", name: "SignIn", component: SignIn },
  { path: "/signup", name: "SignUp", component: SignUp },
  { path: "/confirm-signup", name: "ConfirmSingUp", component: ConfirmSingUp },

  {
    path: "/:pathMatch(.*)*",
    name: "Error404",
    component: Error404,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
