import { apiUrl } from "../../core/config.js";

async function getData(url, bet, guess) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Access-Control-Allow-Origin": "*",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ bet: bet, guess: guess }),
    });

    if (!response.ok) {
        alert("Kolikonheitossa kävi virhe!");
        console.error(response);
        return;
    }

    return await response.json();
}

export async function Coinflip(req) {
    const root = document.querySelector("#root");

    const playerBalance = JSON.parse(localStorage.getItem("userData")).balance;

    root.innerHTML = `
    <div class="game-container">
        <h1>Kolikonheitto</h1>
        <p>Tervetuloa heittämään kolikkoa! Syötä panos ja arvaus!</p>
        <div id="game-area">
            <div class="wrap">
                <div class="left">
                    <div id="coinflip-area">
                        <h2>Kolikko</h2>
                        <div id="coinflip-container">
                        <div class="coin"></div>
                    </div>
                </div>
                <div id="result-area">
                    <h2>Tulos</h2>
                    <p id="outcome"></p>
                    <p id="balance"></p>
                </div>
            </div>
        <div>
        <form class="wrap-me" id="coinflip-form">
            <div class="controls">
                <label for="bet">Panos:</label>
                <input 
                type="number" 
                id="bet" 
                placeholder="Syötä panos" 
                min="1"
                max="${playerBalance}"
                required>
            </div>
            <div class="controls">
                <label for="guess">Arvauksesi:</label>
                <select id="guess">
                    <option value="k">Kruuna 👑</option>
                    <option value="c">Klaava 🍀</option>
                </select>
            </div>
            <input type="submit" value="Heitä kolikkoa!">
        </form>
    </div>
    `;

    const coinflipForm = document.querySelector("#coinflip-form");
    const coin = document.querySelector(".coin");
    const submitBtn = coinflipForm.querySelector("input[type=submit]");

    coinflipForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        submitBtn.disabled = true;

        // reset the coin animation
        coin.style.animation = "none";

        const bet = coinflipForm.querySelector("#bet").value;
        const guess = coinflipForm.querySelector("#guess").value;

        const data = await getData(`${apiUrl}/games/coinflip`, bet, guess);

        // animate the coin
        const flipResult = data.flip[1];
        const resultAngle = flipResult === "kruuna" ? "0deg" : "180deg";

        coin.style.setProperty('--result-angle', resultAngle);
        coin.style.animation = "flip 2s ease-in-out forwards";

        // display outcome when animation ends
        coin.addEventListener("animationend", () => {
            displayOutcome(data);
            submitBtn.disabled = false;
        }, { once: true });
    })
}

function displayOutcome(outcome) {
    const outcomeText = document.querySelector("#outcome");
    const balance = document.querySelector("#balance");

    outcomeText.textContent = `Heiton tulos: ${outcome.flip[1]} ${outcome.flip[2]}. ${outcome.won ? "Voitit!" : "Hävisit..."}`;
    balance.textContent = `Uusi saldosi on: ${outcome.balance}`;
}
