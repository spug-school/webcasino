async function getData(url, bet, diceAmount, guess) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Access-Control-Allow-Origin": "*",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
      body: JSON.stringify({ bet: bet, dice_amount: diceAmount, guess: guess }),
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export async function Dice(req) {
  const root = document.querySelector("#root");

  root.innerHTML = `
      <div class="game-container">
          <h1>Dice Game</h1>
          <p>Welcome to the Dice Game! Place your bet, select dice, and make a guess!</p>
          <div id="game-area">
              <div class="wrap">
                  <div class="left">
                      <div id="dice-area">
                          <h2>Dice Roll</h2>
                          <div id="dice-container"></div>
                        </div>
                        <div id="result-area">
                            <h2>Result</h2>
                            <p id="roll-result"></p>
                            <p id="outcome"></p>
                            <p id="balance"></p>
                        </div>
                    </div>
                    <div>
                        <form class="wrap-me" id="dice-form">
                            <div class="controls">
                                <label for="bet">Bet Amount:</label>
                                <input 
                                type="number" 
                                id="bet" 
                                placeholder="Enter your bet" 
                                min="1"
                                >
                            </div>
                            <div class="controls">
                                <label for="dice-amount">Number of Dice:</label>
                                <input 
                                type="number" 
                                id="dice-amount" 
                            placeholder="Enter dice count (2-4)" 
                            min="2" 
                            max="4"
                            >
                        </div>
                        <div class="controls">
                            <label for="guess">Your Guess:</label>
                            <input 
                            type="number" 
                            id="guess" 
                            placeholder="Guess the sum"
                            >
                        </div>
                        <button>Roll Dice</button>
                    </form>
                </div>
            </div>
        </div>
    </div>    
    `;
  const diceForm = document.querySelector("#dice-form");
  diceForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const bet = event.currentTarget[0].value;
    const diceAmount = event.currentTarget[1].value;
    const guess = event.currentTarget[2].value;
    const data = await getData(
      "http://127.0.0.1:5000/api/games/dice",
      bet,
      diceAmount,
      guess
    );
    console.log(data);
  });
}
