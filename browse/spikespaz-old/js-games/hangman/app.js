const initial_screen = document.getElementById("initial");
const initial_form = initial_screen.getElementsByTagName("input");
const game_screen = document.getElementById("game");
const time = document.getElementById("time").lastChild;
const scaffold = document.getElementById("scaffold").getContext("2d");
const result = document.getElementById("result");
const guessed = document.getElementById("guessed");
const guessed_wrapper = document.getElementById("guessed-wrapper");
const message = document.getElementById("message");

let active = false, seconds = 0, correct = [], hung = [], match; // Initialize variables
// List of body parts, to be removed when added to the scaffold.
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
// Draw main scaffold
// Base
scaffold.moveTo(30, 470);
scaffold.lineTo(370, 470);
// Vertical line
scaffold.moveTo(120, 470);
scaffold.lineTo(120, 30);
// Top line
scaffold.lineTo(250, 30);
// Hook
scaffold.lineTo(250, 90);
// Brace
scaffold.moveTo(185, 30);
scaffold.lineTo(120, 100);
scaffold.stroke();

function drawPart(part) { // Draw specified body part
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

function getTime() { // Return time in min/sec from seconds variable
    return Math.floor(seconds / 60) + "m " + seconds % 60 + "s"
}

initial_form[1].onclick = () => { // The Continue button on initial screen is clicked
    if (initial_form[0].value.split("").some(isLetter)) { // Check if the input contains a letter
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

function alphabetize(text) { // Used for organizing the guessed and missed letters
    return text.split("").sort().join("");
}

function inArray(array, item) { // Check if a character is in a specified array
    return array.indexOf(item) > -1
}

function updateResult() { // Update the displayed sentence/word under the scaffold
    let generated = "";

    let character;
    for (character in match) {
        if (inArray(correct.map(character => character.toLowerCase()), match[character].toLowerCase())) {
            generated += match[character]
        } else if (!isLetter(match[character])) {
            generated += match[character]
        } else {
            generated += "_"
        }
    }

    result.innerText = generated
}

function isLetter(character) { // Check if ASCII character codes are within acceptable ranges (a-Z)
    return character.charCodeAt(0) >= 65 && character.charCodeAt(0) <= 90 ||
        character.charCodeAt(0) >= 97 && character.charCodeAt(0) <= 122
}

document.onkeypress = (event) => {
    if (active && isLetter(event.key) &&
        !inArray(correct, event.key.toLowerCase()) &&
        !inArray(guessed.innerText, event.key.toUpperCase())) {
        message.innerHTML = "Last guess: <code>" + event.key.toUpperCase() + "</code>";

        if (inArray(match.toLowerCase(), event.key.toLowerCase())) { // User got the letter correct
            correct.push(event.key);
            updateResult();

            if (result.innerText === match) { // This means that the letters the user found match the initial string.
                active = false;

                setTimeout(() => {
                    alert("You win!\nTime: " + getTime());
                    location.reload();
                }, 1000);
            }

        } else { // The user missed the letter
            hung.push(body_parts[0]);

            guessed_wrapper.style.display = "block";
            guessed.innerText = alphabetize(guessed.innerText + event.key.toUpperCase());

            drawPart(body_parts[0]);

            if (hung.length === 6) { // Lose, the body parts all on the scaffold
                active = false;

                result.innerText = match;

                setTimeout(() => {
                    alert("You got hung!\nThe message was:\n\"" + match + "\"");
                    location.reload();
                }, 1000);
            }

            body_parts.splice(0, 1);
        }

    } else {
        if (event.keyCode === 13) { // Enter is pressed on initial screen
            initial_form[1].click()
        }
    }
};
