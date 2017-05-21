const canvas = document.getElementById("scaffold");
const drawing = canvas.getContext("2d");
const initial = document.getElementById("initial").getElementsByTagName("input");

let correct;

initial[1].onclick = () => {
    correct = initial[0].value;
    if (!correct) {return;}
    initial[1].parentNode.style.display = "none"
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

drawing.lineWidth = 6;
drawing.lineCap = "round";

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

function letterIsCorrect(character) {
    return correct.indexOf(character) > -1;
}

function letter(code) {
    return String.fromCharCode(code)
}

document.onkeypress = (event) => {
    if (!correct) {return;}

    if (letterIsCorrect(letter(event.keyCode))) {
        console.log("Letter correct.");

    } else {
        scaffold.push(body_parts[0]);
        console.log("Body part lost: " + scaffold);
        body_parts.splice(0, 1);
        console.log("Wrong letter!");

        if (scaffold.length === 6) {
            console.log("You lose!");
        }
    }
};
