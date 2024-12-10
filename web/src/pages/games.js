export function Games(req) {
  const root = document.querySelector("#root");
  console.log(req);
  root.innerHTML = `
    <div class="games-container">
      <h2>Games</h2>
      <p>Choose a game</p>
      <div class="games">
        <div class="game-card">
          <a href="/games/dice">
            <img 
              src="/images/games_page/dicegame.png" 
              alt="Dice"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Dice</h3>
            <p>Roll the dice and test your luck!</p>
          </a>
        </div>

        <div class="game-card">
          <a href="/games/slots">
            <img 
              src="/images/games_page/slotsgame.png" 
              alt="Slots"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Slots</h3>
            <p>Spin the reels and win big!</p>
          </a>
        </div>

        <div class="game-card">
          <a href="/games/roulette">
            <img 
              src="/images/games_page/roulettegame.png" 
              alt="Roulette"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Roulette</h3>
            <p>Place your bets and spin the wheel!</p>
          </a>
        </div>
      </div>
    </div>
  `;
}
