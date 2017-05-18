const table = document.getElementById("cards");
const score = document.getElementById("points").lastChild;
const time = document.getElementById("time").lastChild;
const matches = document.getElementById("matches").lastChild;

const counter = setInterval(() => {
    centiseconds++;
    time.innerText = Math.floor(centiseconds / 10) + "s";
}, 100);

let active = [], pairs = 0, last = 0, points = 0, centiseconds = 0, row, cell, index;

let colors = [
    "red", "red",
    "yellow", "yellow",
    "green", "green",
    "blue", "blue",
    "orange", "orange",
    "purple", "purple",
    "brown", "brown",
    "pink", "pink"
];

function randomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

for (row = 0; row < table.rows.length; row++) {
    for (cell = 0; cell < table.rows[row].cells.length; cell++) {
        index = randomInt(0, colors.length - 1);
        table.rows[row].cells[cell].classList.add(colors[index]);
        colors.splice(index, 1)
    }
}

function activateCard(card) {
    card.classList.add("active");
    card.style.background = card.style.color = card.classList[0];
}

function resetCard(card) {
    card.style.background = "black";
    card.style.color = "white";
    card.classList.remove("active")
}

function checkMatches() {
    if (active[0].classList[0] === active[1].classList[0]) {
        active[0].classList.add("hidden");
        active[1].classList.add("hidden");
        pairs++;
        matches.innerText = pairs;

        points = 1000 - (centiseconds - last);
        score.innerText = points;

        last = centiseconds;

        if (pairs === 8) {
            alert("You win!\nTime: " + centiseconds + "\nPoints: " + points);
            location.reload()
        }

    } else {
        resetCard(active[0]);
        resetCard(active[1]);
        active = []
    }
}

function updateActive(card) {
    if (active.includes(card)) {
        active.splice(active.indexOf(card), 1);
        resetCard(card);

    } else if (active.length < 2) {
        active.push(card);
        activateCard(card);

        if (active.length > 1) {
            setTimeout(checkMatches, 500);
        }

    } else if (active.length > 1) {
        if (active[0].classList.contains("hidden") && active[1].classList.contains("hidden")) {
            resetCard(active[0]);
            resetCard(active[1]);
        }

        active = [card];
        activateCard(card);

    } else {
        active.push(card);
        activateCard(card)
    }
}

alert("You have 80 seconds, go!");

setTimeout(() => {
    clearTimeout(counter);
    alert("Time up!\nYou got " + pairs + "/8 matches.");
    location.reload()
}, 80000);
