const initial_screen = document.getElementById("initial");
const initial_form = initial_screen.getElementsByTagName("input");
const game_screen = document.getElementById("game");
const time = document.getElementById("time").lastChild;
const scaffold = document.getElementById("scaffold").getContext("2d");
const result = document.getElementById("result");
const guessed = document.getElementById("guessed");
const guessed_wrapper = document.getElementById("guessed-wrapper");

let active = false, seconds = 0, correct = [], hung = [], match;
let body_parts = [
    "head",
    "body",
    "left_arm",
    "right_arm",
    "left_leg",
    "right_leg"
];

scaffold.lineWidth = 2;
scaffold.lineCap = "round";
scaffold.translate(0.5, 0.5);

scaffold.moveTo(30, 470);
scaffold.lineTo(370, 470);

scaffold.moveTo(120, 470);
scaffold.lineTo(120, 30);

scaffold.lineTo(250, 30);

scaffold.lineTo(250, 90);
scaffold.stroke();

function drawPart(part) {
    switch (part) {
        case "head":
            scaffold.moveTo(280, 120);
            scaffold.arc(250, 120, 30, 0, Math.PI * 2, true);
            break;
        case "body":
            scaffold.moveTo(250, 150);
            scaffold.lineTo(250, 290);
            break;
        case "left_arm":
            scaffold.moveTo(250, 190);
            scaffold.lineTo(300, 160);
            break;
        case "right_arm":
            scaffold.moveTo(250, 190);
            scaffold.lineTo(200, 160);
            break;
        case "left_leg":
            scaffold.moveTo(250, 290);
            scaffold.lineTo(300, 320);
            break;
        case "right_leg":
            scaffold.moveTo(250, 290);
            scaffold.lineTo(200, 320);
            break;
    }
    scaffold.stroke()
}

function getTime() {
    return Math.floor(seconds / 60) + "m " + seconds % 60 + "s"
}

initial_form[1].onclick = () => {
    if (initial_form[0].value) {
        active = true;
        match = initial_form[0].value;
        initial_screen.style.display = "none";
        game_screen.style.display = "block";

        updateResult();

        setInterval(() => {
            seconds++;
            time.innerText = getTime();
        }, 1000)
    }
};

function alphabetize(text) {
    return text.split("").sort().join("");
}

function inArray(array, item) {
    return array.indexOf(item) > -1
}

function updateResult() {
    let generated = "";

    let character;
    for (character in match) {
        if (inArray(correct.map(character => character.toLowerCase()), match[character].toLowerCase())) {
            generated += match[character]
        } else if (!isLetter(match[character].charCodeAt(0))) {
            generated += match[character]
        } else {
            generated += "_"
        }
    }

    result.innerText = generated
}

function isLetter(code) {
    return code >= 65 && code <= 90 || code >= 97 && code <= 122
}

document.onkeypress = (event) => {
    if (active && isLetter(event.keyCode)) {
        if (inArray(match.toLowerCase(), event.key.toLowerCase())) {
            correct.push(event.key);
            updateResult();

            if (result.innerText === match) {
                setTimeout(() => {
                    alert("You win!\nTime: " + getTime());
                    location.reload();
                }, 1000);
            }

        } else if (!inArray(guessed.innerText, event.key.toUpperCase())){
            hung.push(body_parts[0]);

            guessed_wrapper.style.display = "block";
            guessed.innerText = alphabetize(guessed.innerText + event.key.toUpperCase());

            drawPart(body_parts[0]);

            if (hung.length === 6) {
                result.innerText = match;

                setTimeout(() => {
                    alert("You got hung!\nThe message was:\n\"" + match + "\"");
                    location.reload();
                }, 1000);
            }

            body_parts.splice(0, 1);
        }

    } else {
        if (event.keyCode === 13) {
            initial_form[1].click()
        }
    }
};
