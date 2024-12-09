import { getGameHistory, getPlayerData } from "../utils/fetchUtils";

export async function Profile(req) {
  const root = document.querySelector("#root");

  const playerData = await getPlayerData(localStorage.getItem("user_id"));
  console.log(playerData)
  const gameHistory = await getGameHistory();

  root.innerHTML = `
    <div class="container">
      <h2>Omat tiedot</h2>
      <table id="profile-info">
        <thead>
          <tr>
            <th>Käyttäjänimi</th>
            <th>Saldo</th>
            <th>Pelejä pelattu</th>
            <th>Voitetut pelit</th>
            <th>Hävityt pelit</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>${playerData.username}</td>
            <td>${playerData.balance}</td>
            <td>${playerData.games_played}</td>
            <td>${playerData.games_won}</td>
            <td>${playerData.games_lost}</td>
          </tr>
        </tbody>
      </table>
      <h2>Viimeisimmät pelisi</h2>
      <table id="game-history">
        <thead>
          <tr>
            <th>Peli</th>
            <th>Ajankohta</th>
            <th>Panos</th>
            <th>Voiton määrä</th>
          </tr>
        </thead>
        <tbody>
          ${gameHistory.map((game) => `
              <tr>
                <td>${game.name}</td>
                <td>${game.played_at}</td>
                <td>${game.bet}</td>
                <td>${game.win_amount}</td
              </tr>
            `
          ).join("")}
        </tbody>
      </table>
    </div>
    `;
}