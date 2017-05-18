const table = document.getElementById("grid");
const turn = document.getElementById("turn").lastChild;
const time = document.getElementById("time").lastChild;

const counter = setInterval(() => {
    centiseconds++;
    time.innerText = getSeconds() + "s";
}, 100);

let next = "x", grid = [], centiseconds = 0, row, cell, index;

function randomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

for (row = 0; row < table.rows.length; row++) {
    for (cell = 0; cell < table.rows[row].cells.length; cell++) {
        grid.push(table.rows[row].cells[cell])
    }
}

function getSeconds() {
    return Math.floor(centiseconds / 10)
}

function updateCell(cell) {
    console.log(cell.innerText);
    if (!cell.innerText) {
        cell.innerText = next;
        if (next === "x") {
            next = "o"
        } else {
            next = "x"
        }
        cell.classList.add("filled");
    }
}

setTimeout(() => {
    clearTimeout(counter);
    location.reload()
}, 80000);
