export function Leaderboard(req) {
  const root = document.querySelector("#root");
  console.log(req);
  root.innerHTML = `
    <div class="table-container">
    <table>
    <thead>
        <tr>
            <th>Rank</th>
            <th>Username</th>
            <th>Balance</th>
            <th>Games Played</th>
            <th>Games Won</th>
            <th>Games Lost</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Bob Ross</td>
            <td>100</td>
            <td>10</td>
            <td>5</td>
            <td>5</td>
         
        </tr>
        <tr>
            <td>2</td>
            <td>Bob Ross</td>
            <td>100</td>
            <td>10</td>
            <td>5</td>
            <td>5</td>
          
        </tr>
  
        <!-- Add more rows as needed -->
  
    </tbody>
  
  </table>
  </div>
  `;
}
