import "./styles.css";
import { Router } from "./core/simpleRouter.js";
import { Games } from "./pages/games.js";
import { Home } from "./pages/home.js";
import { Login } from "./pages/login.js";
import { Profile } from "./pages/profile.js";
import { Leaderboard } from "./pages/leaderboard.js";
import { Dice } from "./pages/games/dice.js";

export const router = new Router();

const token = localStorage.getItem("token");

if (!token && window.location.pathname !== "/login") {
  const navbar = document.querySelector(".navbar");
  navbar.style = "display: none";
  window.location.href = "/login";
}

if (token) {
  const user = document.querySelector("#user");
  user.href = `/logout`;
  user.innerHTML = `logout`;
}

router.get("/", (req) => Home(req));
router.get("/login", (req) => Login(req));
router.get("/logout", (req) => {
  fetch("http://127.0.0.1:5000/api/logout", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
  });
  localStorage.removeItem("token");
  window.location.href = "/login";
});
router.get("/profile", (req) => Profile(req));
router.get("/leaderboard", (req) => Leaderboard(req));
router.get("/games", (req) => Games(req));
router.get("/games/dice", (req) => Dice(req));

router.init();
