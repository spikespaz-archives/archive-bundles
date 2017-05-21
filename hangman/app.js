const drawing = document.getElementById("scaffold").getContext("2d");
const game = document.getElementById("game");
const initial = document.getElementById("initial").getElementsByTagName("input");
const result = document.getElementById("result");
const guessed = document.getElementById("guessed");
const time = document.getElementById("time").lastChild;

let acceptable;
let correct = [];
let seconds = 0;

initial[1].onclick = () => {
    acceptable = initial[0].value;
    if (!acceptable) {return;}
    initial[1].parentNode.style.display = "none";
    game.style.display = "block";
    updateResult();

    setInterval(() => {
        seconds++;
        time.innerText = Math.floor(seconds / 60) + "m " + seconds % 60 + "s";
    }, 1000)
};

let body_parts = [
    "head",
    "body",
    "left_arm",
    "right_arm",
    "left_leg",
    "right_leg"
];

let scaffold = [];

drawing.lineWidth = 2;
drawing.lineCap = "round";
drawing.translate(0.5, 0.5);

// Base
drawing.moveTo(30, 470);
drawing.lineTo(370, 470);
// Vertical Line
drawing.moveTo(120, 470);
drawing.lineTo(120, 30);
// Top Line
drawing.lineTo(250, 30);
// Hook
drawing.lineTo(250, 90);
drawing.stroke();


function drawPart(part) {
    switch (part) {
        case "head":
            drawing.moveTo(280, 120);
            drawing.arc(250, 120, 30, 0, Math.PI * 2, true);
            break;
        case "body":
            drawing.moveTo(250, 150);
            drawing.lineTo(250, 290);
            break;
        case "left_arm":
            drawing.moveTo(250, 190);
            drawing.lineTo(300, 160);
            break;
        case "right_arm":
            drawing.moveTo(250, 190);
            drawing.lineTo(200, 160);
            break;
        case "left_leg":
            drawing.moveTo(250, 290);
            drawing.lineTo(300, 320);
            break;
        case "right_leg":
            drawing.moveTo(250, 290);
            drawing.lineTo(200, 320);
            break;
    }
    drawing.stroke()
}

function letterIsCorrect(compare, character) {
    if (Array.isArray(compare)) {
        compare = compare.map((letter) => letter.toUpperCase())
    } else {
        compare.toUpperCase()
    }

    return compare.indexOf(character.toUpperCase()) > -1;
}

function getLetter(code) {
    return String.fromCharCode(code)
}

function updateResult() {
    let generated = "";

    let character;
    for (character in acceptable) {
        if (letterIsCorrect(correct, acceptable[character])) {
            generated += acceptable[character]
        } else if (acceptable[character] === " ") {
            generated += " "
        } else {
            generated += "_"
        }
    }

    result.innerText = generated;
}

document.onkeypress = (event) => {
    if (!acceptable) {
        if (event.keyCode === 13) {
            initial[1].click()
        }

        return;
    }

    if (letterIsCorrect(acceptable, getLetter(event.keyCode))) {
        correct.push(getLetter(event.keyCode));
        updateResult();

        if (result.innerText === acceptable) {
            alert("You won!");
            location.reload()
        }

    } else {
        scaffold.push(body_parts[0]);

        if (!guessed.innerText) {
            document.getElementsByClassName("guessed")[0].style.display = "block";
        }

        guessed.innerText += getLetter(event.keyCode).toUpperCase();

        drawPart(body_parts[0]);

        if (scaffold.length === 6) {
            setTimeout(() => {
                alert("You got hung!");
                location.reload();
            }, 1000);
        }

        body_parts.splice(0, 1);
    }
};
