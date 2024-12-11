import { apiUrl } from "../../core/config.js";

async function getData(url, bet, number, color) {
  const response = await fetch(`${apiUrl}${url}`, {
    method: "POST",
    headers: {
      "Access-Control-Allow-Origin": "*",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      bets: bet,
      color_guesses: color,
      number_guesses: number,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export async function Roulette(req) {
  const root = document.querySelector("#root");

  const playerBalance = localStorage.getItem("userData").balance;

  root.innerHTML = `
      <div class="game-container">
          <h1>Roulette</h1>
          <p>Tervetuloa heittämään kolikkoa! Syötä panos ja arvaus!</p>
          <div id="game-area">
              <div class="wrap">
                  <div class="left">
                  <div id="result-area">
                          <h2>Ruletti</h2>
                          <div class="roulette-container"></div>
                        </div>
                        <div id="result-area">
                            <h2>Tulos</h2>
                            <p id="outcome"></p>
                            <p id="balance"></p>
                        </div>
                    </div>
                    <div>
          <form class="wrap-me" id="roulette-form">
              <label for="bet">Arvo</label>
              <input type="number" id="bet" name="bet" placeholder="Syötä panos" min="1" max="${playerBalance}">
              <label for="number">Arvo</label>
              <input type="number" id="number" name="number" placeholder="Syötä arvo" min="1" max="36">
              <label for="color">Väri</label>
              <select id="color">
                <option value="p">Red</option>
                <option value="m">Black</option>
                <option value="v">Green</option>
              </select>
              <button id="play">Play</button>
          </form>
          </div>
            </div>
        </div>
    </div> 
       
    `;

  let wheelnumbersAC = [
    0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10,
    23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32,
  ];

  const rouletteContainer = document.querySelector(".roulette-container");

  let wheel = document.createElement("div");
  wheel.setAttribute("class", "wheel");

  const outerRim = document.createElement("div");
  outerRim.setAttribute("class", "outerRim");
  wheel.append(outerRim);

  const numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
  ];
  for (let i = 0; i < numbers.length; ++i) {
    let a = i + 1;
    let spanClass = numbers[i] < 10 ? "single" : "double";
    let sect = document.createElement("div");
    sect.setAttribute("id", "sect" + a);
    sect.setAttribute("class", "sect");
    let span = document.createElement("span");
    span.setAttribute("class", spanClass);
    span.innerText = numbers[i];
    sect.append(span);
    let block = document.createElement("div");
    block.setAttribute("class", "block");
    sect.append(block);
    wheel.append(sect);
  }

  let pocketsRim = document.createElement("div");
  pocketsRim.setAttribute("class", "pocketsRim");
  wheel.append(pocketsRim);

  let ballTrack = document.createElement("div");
  ballTrack.setAttribute("class", "ballTrack");
  let ball = document.createElement("div");
  ball.setAttribute("class", "ball");
  ballTrack.append(ball);
  wheel.append(ballTrack);

  let pockets = document.createElement("div");
  pockets.setAttribute("class", "pockets");
  wheel.append(pockets);

  let cone = document.createElement("div");
  cone.setAttribute("class", "cone");
  wheel.append(cone);
  rouletteContainer.append(wheel);

  function spinWheel(winningSpin) {
    // let degree = 0;
    // for (let i = 0; i < wheelnumbersAC.length; ++i) {
    //   if (wheelnumbersAC[i] == winningSpin) {
    //     degree = i * 9.73;
    //   }
    // }

    const sectionIndex = wheelnumbersAC.indexOf(winningSpin);
    const degreePerSection = 360 / wheelnumbersAC.length;
    const totalRotation =
      360 * 5 + sectionIndex * degreePerSection + degreePerSection / 2;

    // ballTrack.style.transform = `rotate(-${totalRotation}deg)`;

    ballTrack.classList.add("ballTrackAni1");
    setTimeout(() => {
      ballTrack.classList.remove("ballTrackAni1");
      const style = document.createElement("style");
      style.innerText = `
          @keyframes ballStop {
            from { transform: rotate(0deg); }
            to { transform: rotate(-${totalRotation}deg); }
          }
        `;
      document.head.appendChild(style);
      ballTrack.style.cssText = `animation: ballStop 4s linear forwards;`;
    }, 2000);

    setTimeout(() => {
      ballTrack.style.cssText = `transform: rotate(-${totalRotation}deg);`;
      //   ballTrack.style.cssText = ``;
    }, 6000);
  }

  const rouletteForm = document.querySelector("#roulette-form");
  rouletteForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const bet = event.currentTarget[0].value;
    const number = event.currentTarget[1].value;
    const color = event.currentTarget[2].value;

    const data = await getData("/games/roulette", bet, number, color);

    spinWheel(data.roll.number);
    setTimeout(() => {
      displayOutcome(data);
    }, 6000);
    console.log(data);
  });
}

function displayOutcome(outcome) {
  const outcomeText = document.querySelector("#outcome");
  const balance = document.querySelector("#balance");

  outcomeText.textContent = `Heiton summa: ${outcome.win_amount}, ${
    outcome.won ? "Voitit!" : "Hävisit..."
  }`;
  balance.textContent = `Uusi saldo: ${outcome.balance}`;
}
