"use strict";

let control = document.querySelector("#control");
let renderWindow = document.querySelector("#render");
let secondaryTitle = document.querySelector("#secondary");

let dealerHand = [];
let playerHand = [];
let playerPass = false;

async function drawTable () {
    if (playerPass) {
        dealerHand.forEach((img) => {
            const image = document.createElement("img");
            image.src = img;

        })
    }
}

function twentyOneForm() {
    control.textContent = ""
    const formTwentyOne = document.createElement("form");
    formTwentyOne.id = "twentyOneForm";
    formTwentyOne.method = "post";
    formTwentyOne.action = "/data/";
    formTwentyOne.classList.add("activeForm");
    const yesButton = document.createElement("button");
    yesButton.name = "yesButton";
    yesButton.value = "Yes";
    yesButton.innerHTML = "Yes";
    formTwentyOne.appendChild(yesButton);
    const noButton = document.createElement("button");
    noButton.name = "noButton";
    noButton.value = "No";
    noButton.innerHTML = "No";
    formTwentyOne.appendChild(noButton);
    control.appendChild(formTwentyOne);
    formTwentyOne.addEventListener("submit", (event) => {
        event.preventDefault();
        const data = {command: ""}

        if (formTwentyOne.action === "yes") {
            data.command = "Yes";
        } else if (formTwentyOne.action === "no") {
            data.command = "No";
        }
        try {
            fetch(async () => {
                const rawResponse = await fetch("http://localhost:5000", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const content = await rawResponse.json();
            })
        } catch (e) {
            console.log(e)
        }
    })
}

twentyOneForm()