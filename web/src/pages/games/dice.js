async function getData(url, bet, diceAmount, guess) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Access-Control-Allow-Origin": "*",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ bet: bet, dice_amount: diceAmount, guess: guess }),
  });

  if (!response.ok) {
    alert("Nopanheitossa kävi virhe!");
    console.error(response);
    return;
  }

  return await response.json();
}

export async function Dice(req) {
  const root = document.querySelector("#root");

  const playerBalance = JSON.parse(localStorage.getItem("userData")).balance;

  root.innerHTML = `
      <div class="game-container">
          <h1>Nopanheitto</h1>
          <p>Tervetuloa nopanheittoon! Syötä panos, valitse noppien määrä ja arvaa näiden noppien heiton summa!</p>
          <div id="game-area">
              <div class="wrap">
                  <div class="left">
                      <div id="dice-area">
                          <h2>Nopat</h2>
                          <div id="dice-container"></div>
                        </div>
                        <div id="result-area">
                            <h2>Tulos</h2>
                            <p id="roll-result"></p>
                            <p id="outcome"></p>
                            <p id="balance"></p>
                        </div>
                    </div>
                    <div>
                        <form class="wrap-me" id="dice-form">
                            <div class="controls">
                                <label for="bet">Panos:</label>
                                <input 
                                type="number" 
                                id="bet" 
                                placeholder="Syötä panos" 
                                min="1"
                                max="${playerBalance}"
                                required
                                >
                            </div>
                            <div class="controls">
                                <label for="dice-amount">Noppien määrä</label>
                                <input 
                                type="number" 
                                id="dice-amount" 
                            placeholder="Nopat (2-4)" 
                            min="2" 
                            max="4"
                            required
                            >
                        </div>
                        <div class="controls">
                            <label for="guess">Arvauksesi:</label>
                            <input 
                            type="number" 
                            id="guess" 
                            placeholder="Arvaa summa"
                            min="2"
                            max="24"
                            required>
                        </div>
                        <input type="submit" value="Heitä nopat!">
                    </form>
                </div>
            </div>
        </div>
    `;

  const outcomeText = document.querySelector("#outcome");
  const balance = document.querySelector("#balance");
  const rollResult = document.querySelector("#roll-result");

  const diceForm = document.querySelector("#dice-form");
  const submitBtn = diceForm.querySelector("input[type=submit]");

  diceForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    submitBtn.disabled = true;

    outcomeText.innerHTML = '';
    balance.innerHTML = '';
    rollResult.innerHTML = '';

    const bet = event.currentTarget[0].value;
    const diceAmount = event.currentTarget[1].value;
    const guess = event.currentTarget[2].value;
    const data = await getData(
      "http://127.0.0.1:5000/api/games/dice",
      bet,
      diceAmount,
      guess
    );
    // clear the dice container
    const diceContainer = document.querySelector("#dice-container");
    diceContainer.innerHTML = "";

    // create images of the dice rolls
    const diceRolls = data.dice_rolls;
    diceRolls.forEach((diceValue, index) => {
      setTimeout(() => {
        createDiceElement(diceValue, diceContainer);
        if (index === diceRolls.length - 1) {
          rollResult.innerHTML = `Noppien arvot ovat ${diceRolls.join(", ")}`
          outcomeText.innerHTML = `Heiton summa: ${data.sum}, ${data.won ? "Voitit!" : "Hävisit..."}`
          balance.innerHTML = `Uusi saldo: ${data.balance}`
          submitBtn.disabled = false;
        }
      }, index * 750);
    });
  });
}

function createDiceElement(diceValue, target) {
  const diceWrapper = document.createElement("div");
  diceWrapper.classList.add("dice");

  const diceImg = document.createElement("img");
  diceImg.src = `/images/dice/side_${diceValue}_pips.png`;
  diceImg.alt = `dice ${diceValue}`;
  diceWrapper.appendChild(diceImg);

  target.appendChild(diceWrapper);
}