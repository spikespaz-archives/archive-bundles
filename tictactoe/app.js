const table = document.getElementById("grid");
const turn = document.getElementById("turn").lastChild;
const time = document.getElementById("time").lastChild;

let next = "x", grid = [], seconds = 0, row, cell;

for (row = 0; row < table.rows.length; row++) {
    for (cell = 0; cell < table.rows[row].cells.length; cell++) {
        grid.push(table.rows[row].cells[cell])
    }
}

function updateNext() {
    if (next === "x") {
        next = "o"
    } else {
        next = "x"
    }
    turn.innerText = next.toUpperCase()
}

function updateCell(cell) {
    console.log(cell.innerText);
    if (!cell.innerText) {
        cell.innerText = next;
        
        cell.classList.add("filled");
        updateNext()
    }
}

setInterval(() => {
    seconds++;
    time.innerText = seconds + "s";
}, 1000);
