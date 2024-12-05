export function Games(req) {
  const root = document.querySelector("#root");
  console.log(req);
  root.innerHTML = `
    <div id="title">
      <h1>Games</h1>
      <h2>Choose a game</h2>
    </div>
    <div>
      <h3>Slots</h3>
      <p>Description</p>
    </div>
    <div>
      <h3>Roulette</h3>
      <p>Description</p>
    </div>
    <div>
      
  `;
}
