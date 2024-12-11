export function Games(req) {
  const root = document.querySelector("#root");
  console.log(req);
  root.innerHTML = `
    <div class="games-container">
      <h2>Pelit</h2>
      <p>Valitse Peli</p>
      <div class="games">
        <div class="game-card">
          <a href="/games/dice">
            <img 
              src="/images/games_page/dicegame.png" 
              alt="Nopanheitto"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Nopanheitto</h3>
            <p>Pelissä heitetään pelaajan valitsemaa määrää noppia. Pelaaja arvaa näiden noppien heiton summan.</p>
          </a>
        </div>

        <div class="game-card">
          <a href="/games/slots">
            <img 
              src="/images/games_page/slotsgame.png" 
              alt="Hedelmäpeli"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Hedelmäpeli</h3>
            <p>Vedä vivusta ja voita isosti!</p>
          </a>
        </div>

        <div class="game-card">
          <a href="/games/coinflip">
            <img 
              src="/images/games_page/coinflipgame.png" 
              alt="Kolikonheitto"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Kolikonheitto</h3>
            <p>Heitä kolikko ja anna kohtalon päättää!</p>
          </a>
        </div>
        
        <div class="game-card">
          <a href="/games/roulette">
            <img 
              src="/images/games_page/roulettegame.png" 
              alt="Ruletti"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Ruletti</h3>
            <p>Pyörän ympäri kiertää, mihin onni laskeutuu, kuka tietää?</p>
          </a>
        </div>
        
        <div class="game-card">
          <a href="/games/ventti">
            <img 
              src="/images/games_page/venttigame.png" 
              alt="Ventti"
              style="width: 100%; border-radius: 0.5rem;"
            >
            <h3>Ventti</h3>
            <p>Pelaa korttisi oikein ja voita jakajan!</p>
          </a>
        </div>
      </div>
    </div>
  `;
}
