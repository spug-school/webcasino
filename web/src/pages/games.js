export function Games(req) {
  const root = document.querySelector("#root");
  console.log(req);
  root.innerHTML = `
    <h2>Games</h2>
    <p>Choose a game</p>
    <div class="games">
      <a href="/games/dice">
      <figure>
        <img 
          src="https://cdn.pixabay.com/photo/2022/03/01/22/02/dice-7195733_960_720.png" 
          alt="Dice">
        <h3>Dice</h3>
        <p>Description</p>
      </figure>
      </a>
      <div>
        <h3>Slots</h3>
        <p>Description</p>
      </div>
      <div>
        <h3>Roulette</h3>
        <p>Description</p>
      </div>
      <div>
    </div>
    <div>
      
  `;
}
