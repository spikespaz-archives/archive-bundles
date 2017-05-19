const table = document.getElementById("grid");
const turn = document.getElementById("turn").lastChild;
const time = document.getElementById("time").lastChild;

let next = "x", grid = [], seconds = 0, row, cell, full;

for (row = 0; row < table.rows.length; row++) {
    for (cell = 0; cell < table.rows[row].cells.length; cell++) {
        grid.push(table.rows[row].cells[cell])
    }
}

function getTime() {
    return Math.floor(seconds / 60) + "m " + seconds % 60 + "s"
}

function updateNext() {
    if (next === "x") {
        next = "o"
    } else {
        next = "x"
    }
    turn.innerText = next.toUpperCase()
}

function checkWin() {
    for (let i = 0; i < 3; i++) {
        if ((grid[i].innerText === grid[i + 1].innerText && grid[i + 1].innerText === grid[i + 2].innerText && grid[i].innerText !== "") ||
            (grid[i].innerText === grid[i + 3].innerText && grid[i + 3].innerText === grid[i + 6].innerText && grid[i].innerText !== "")) {
            return 1
        }
    }
    
    if ((grid[0].innerText === grid[4].innerText && grid[4].innerText === grid[8].innerText && grid[0].innerText !== "") ||
        (grid[2].innerText === grid[4].innerText && grid[4].innerText === grid[6].innerText && grid[2].innerText !== "")) {
        return 1
        
    } else {
        full = 0;

        grid.forEach((cell) => {
            if (cell.innerText !== "") {
                full++
            }
        });

        if (full === 9) {
            return 2
        } else {
            return 0
        }
    }
}

function updateCell(cell) {
    if (!cell.innerText) {
        cell.innerText = next;
        
        cell.classList.add("filled");
        
        if (checkWin() === 1) {
            setTimeout(() => {
                alert("Winner: " + next.toUpperCase() + "\nTime: " + getTime());
                location.reload()
                }, 200)
        } else if (checkWin() === 2) {
            setTimeout(() => {
                alert("Nobody wins!\nTime: " + getTime());
                location.reload()
            }, 200)
        } else {
            updateNext();
        }
    }
}

setInterval(() => {
    seconds++;
    time.innerText = getTime();
}, 1000);
