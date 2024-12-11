import { getGameHistory } from "../utils/fetchUtils.js";

export async function Profile(req) {
  const root = document.querySelector("#root");

  const playerData = JSON.parse(localStorage.getItem("userData"));
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
      <br>
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
                <td>${convertDate(game.played_at)}</td>
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

function convertDate(dateString) {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  const formattedDate = `${day}.${month}.${year} klo ${hours}:${minutes}:${seconds}`;
  
  return formattedDate;
}