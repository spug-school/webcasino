import "./styles.css";
import { Router } from "./core/simpleRouter.js";
import { Games } from "./pages/games.js";
import { Home } from "./pages/home.js";
import { Login } from "./pages/login.js";
import { Profile } from "./pages/profile.js";
import { Leaderboard } from "./pages/leaderboard.js";
import { Dice } from "./pages/games/dice.js";
import { Coinflip } from "./pages/games/coinflip.js";

import { getPlayerData } from "./utils/fetchUtils.js";
import { Roulette } from "./pages/games/roulette.js";

export const router = new Router();

const token = localStorage.getItem("token");
const user_id = localStorage.getItem("user_id");

if (!token && window.location.pathname !== "/login") {
  const navbar = document.querySelector(".navbar");
  navbar.style = "display: none";
  window.location.href = "/login";
}

if (token && user_id) {
  const user = document.querySelector("#user");
  user.href = `/logout`;
  user.innerHTML = `Poistu pelistä`;

  if (!localStorage.getItem("userData")) {
    getPlayerData(user_id).then((data) => {
      localStorage.setItem("userData", JSON.stringify(data));
    });
  }
  
  const userData = JSON.parse(localStorage.getItem("userData"));
  const welcomeText = document.querySelector("#user-welcome");
  welcomeText.innerHTML = `Tervetuloa, <b>${userData.username}</b>. Saldosi on ${userData.balance}`;
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
  localStorage.removeItem("user_id");
  localStorage.removeItem("userData");
  window.location.href = "/login";
});
router.get("/profile", (req) => Profile(req));
router.get("/leaderboard", (req) => Leaderboard(req));
router.get("/games", (req) => Games(req));
router.get("/games/dice", (req) => Dice(req));
router.get("/games/coinflip", (req) => Coinflip(req));
router.get("/games/roulette", (req) => Roulette(req));

router.init();
