"use strict";

let control = document.querySelector("#control");
let renderWindow = document.querySelector("#render");
let secondaryTitle = document.querySelector("#secondary");
let messageDisplay = document.querySelector("#communication");
let running = false;

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
    yesButton.id = "yes"
    formTwentyOne.appendChild(yesButton);
    const noButton = document.createElement("button");
    noButton.name = "noButton";
    noButton.value = "No";
    noButton.innerHTML = "No";
    noButton.id = "no"
    formTwentyOne.appendChild(noButton);
    control.appendChild(formTwentyOne);

    formTwentyOne.addEventListener("click", (event) => {
        event.preventDefault();
        const clickedButton = event.target;
        const answerYes = formTwentyOne.querySelector("#yes");
        const answerNo = formTwentyOne.querySelector("#no");
        if (clickedButton.id === "yes") {
            console.log(answerYes.id)
            fetch('/data/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'input':answerYes.value}),
            })
            .then(response => response.json())
            .then(data => {
                renderWindow.innerHTML = "";
                messageDisplay.innerHTML = "";
                const dealerHand = data.data.dealer_hand;
                const playerHand = data.data.player_hand;
                const playerPass = data.data.player_pass;
                const lineBreak = document.createElement("br");
                const messageList = data.data.message;

                messageList.forEach(message => {
                    const messageObject = document.createElement("li");
                    messageObject.textContent = message;
                    messageDisplay.appendChild(messageObject);
                })
                dealerHand.forEach((dealerCard) => {
                    if (!playerPass) {
                        const image = document.createElement("img");
                        image.src = `/frontend/img/card_0.png`;
                        image.alt = "Back of playing card";
                        renderWindow.appendChild(image);
                    } else {
                        const image = document.createElement("img");
                        image.src = `/frontend/img/` + dealerCard.suit + `_` + dealerCard.rank + `.png`;
                        image.alt = dealerCard.rank + " of " + dealerCard.suit;
                        renderWindow.appendChild(image);
                    }
                })
                renderWindow.appendChild(lineBreak);

                playerHand.forEach(playerCard => {
                    const image = document.createElement("img");
                    image.src = image.src = `/frontend/img/` + playerCard.suit + `_` + playerCard.rank + `.png`;
                    image.alt = playerCard.rank + " of " + playerCard.suit;
                    renderWindow.appendChild(image);
                })
            })
            .catch(error => console.log(error));
        } else if (clickedButton.id === "no") {
            console.log(answerNo.id)
            fetch('/data/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({'input':answerNo.value}),
            })
                .then(response => response.json())
                .then(data => {
                    renderWindow.innerHTML = "";
                    messageDisplay.innerHTML = "";
                    const dealerHand = data.data.dealer_hand;
                    const playerHand = data.data.player_hand;
                    const playerPass = data.data.player_pass;
                    const messageList = data.data.message;

                    messageList.forEach(message => {
                        const messageObject = document.createElement("li");
                        messageObject.textContent = message;
                        messageDisplay.appendChild(messageObject);
                    })
                    const lineBreak = document.createElement("br");
                    dealerHand.forEach((dealerCard) => {
                        if (playerPass) {
                            const image = document.createElement("img");
                            image.src = "/frontend/img/" + dealerCard.suit + "_" + dealerCard.rank + ".png";
                            image.alt = dealerCard.rank + " of " + dealerCard.suit;
                            renderWindow.appendChild(image);
                        } else {
                            const image = document.createElement("img");
                            image.src = "/frontend/img/card_0.png";
                            image.alt = "Back of playing card";
                            renderWindow.appendChild(image);
                        }
                    })
                    renderWindow.appendChild(lineBreak);

                    playerHand.forEach(playerCard => {
                        const image = document.createElement("img");
                        image.src = "/frontend/img/" + playerCard.suit + "_" + playerCard.rank + ".png";
                        image.alt = playerCard.rank + " of " + playerCard.suit;
                        renderWindow.appendChild(image);
                    })
                })
                .catch(error => console.log(error));
        }
    })
}

twentyOneForm()