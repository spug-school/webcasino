import { getPlayerData } from "../../utils/fetchUtils.js";

export async function Slots(req) {
    const root = document.querySelector("#root");

    const playerBalance = localStorage.getItem("userData").balance;

    root.innerHTML = `
    <div class="game-container">
      <h1>Hedelmäpeli</h1>
      <p>Tervetuloa hedelmäpeliin! Syötä panos ja aloita peli!</p>
      <div id="game-area">
        <div id="slots-area">
          <div id="slot-machine">
            <div class="reel">🍑</div>
            <div class="reel">🍑</div>
            <div class="reel">🍑</div>
            <div class="reel">🍑</div>
          </div>
        </div>
        <form id="slots-form">
          <label for="bet">Panos:</label>
          <input 
            type="number" 
            id="bet" 
            placeholder="Syötä panos" 
            min="1"
            max="${playerBalance}"
            required
          >
          <button type="submit">Aloita peli!</button>
        </form>
        <div id="result-area">
          <p id="outcome"></p>
          <p id="balance"></p>
        </div>
      </div>
    </div>
  `;

    const slotsForm = document.querySelector("#slots-form");
    slotsForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const bet = parseInt(document.querySelector("#bet").value);
        const response = await fetch("http://127.0.0.1:5000/api/games/slots", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ bet: bet }),
        });

        if (!response.ok) {
            alert("Error spinning the slot machine!");
            return;
        }

        const data = await response.json();
        console.log("Response data:", data);

        const reels = document.querySelectorAll(".reel");
        data.spin_result.forEach((symbol, index) => {
            reels[index].textContent = symbol;
        });

        console.log("Reel elements:", reels);

        document.querySelector("#outcome").textContent = data.won
            ? `Voitit! Saldosi kasvoi ${data.win_amount} yksikköä.`
            : "Hävisit panoksesi.";
        document.querySelector("#balance").textContent = `Uusi saldo: ${data.balance}`;

        const userData = await getPlayerData(localStorage.getItem("user_id"));
        localStorage.setItem("userData", JSON.stringify(userData));
    });
}
