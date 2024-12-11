function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function Slots(req) {
  const root = document.querySelector("#root");

  const playerBalance = JSON.parse(localStorage.getItem("userData")).balance;

  // Array of slot icons
  const symbols = ['🍑', '🍌', '🍒', '🍏', '🍇'];

  root.innerHTML = `
<div class="center-container">
  <div class="game-container game-container-slots">
    <h1>Hedelmäpeli</h1>
    <p>Tervetuloa hedelmäpeliin! Syötä panos ja aloita peli!</p>
    <div id="game-area">
      <div id="slots-area">
        <div id="slot-machine">
          <div class="reel">🍑</div>
          <div class="reel">🍌</div>
          <div class="reel">🍒</div>
          <div class="reel">🍏</div>
        </div>
      </div>
      <form id="slots-form">
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
        <h2>Tulos</h2>
        <p id="outcome"></p>
        <p id="balance"></p>
      </div>
    </div>
  </div>
</div>
`;

  const outcome = document.querySelector("#outcome");
  const balance = document.querySelector("#balance");

  console.log("hips")

  const slotsForm = document.querySelector("#slots-form");
  slotsForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    outcome.innerHTML = "";
    balance.innerHTML = "";

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

    await spinReels(reels, symbols, data.spin_result);

    document.querySelector("#outcome").textContent = data.won
      ? `Voitit! Saldosi kasvoi ${data.win_amount} pistettä.`
      : "Hävisit panoksesi.";
    document.querySelector("#balance").textContent = `Uusi saldo: ${data.balance}`;
  });

}

async function spinReels(reels, symbols, finalResult) {
  const spinTime = [1000, 1200, 1400, 1600];
  const intervalTime = 100;

  for (let i = 0; i < reels.length; i++) {
    const reel = reels[i];

    const start = performance.now();

    while (performance.now() - start < spinTime[i]) {
      const randomSymbol = symbols[Math.floor(Math.random() * symbols.length)];
      reel.textContent = randomSymbol;
      await sleep(intervalTime);
    }

    reel.textContent = finalResult[i];
  }
}