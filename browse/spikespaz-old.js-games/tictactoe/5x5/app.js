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
    for (cell = 0; cell < 5; cell++) {
        if ((grid[cell * 5].innerText === grid[cell * 5 + 1].innerText &&
            grid[cell * 5 + 1].innerText === grid[cell * 5 + 2].innerText &&
            grid[cell * 5 + 2].innerText === grid[cell * 5 + 3].innerText &&
            grid[cell * 5 + 3].innerText === grid[cell * 5 + 4].innerText && grid[cell * 5].innerText) ||
            (grid[cell].innerText === grid[cell + 5].innerText &&
            grid[cell + 5].innerText === grid[cell + 10].innerText &&
            grid[cell + 10].innerText === grid[cell + 15].innerText &&
            grid[cell + 15].innerText === grid[cell + 20].innerText && grid[cell].innerText)) {
            return 1
        }
    }
    
    if ((grid[0].innerText === grid[6].innerText &&
        grid[6].innerText === grid[12].innerText &&
        grid[12].innerText === grid[18].innerText &&
        grid[18].innerText === grid[24].innerText && grid[0].innerText) ||
        (grid[4].innerText === grid[8].innerText &&
        grid[8].innerText === grid[12].innerText &&
        grid[12].innerText === grid[16].innerText &&
        grid[16].innerText === grid[20].innerText && grid[4].innerText)) {
        return 1
        
    } else {
        full = 0;

        for (cell in grid) {
            if (grid[cell].innerText) {
                full++
            }
        }

        if (full === 25) {
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

        switch (checkWin()) {
            case 2:
                setTimeout(() => {
                    alert("Nobody wins!\nTime: " + getTime());
                    location.reload()
                }, 200);
                break;
            case 1:
                setTimeout(() => {
                    alert("Winner: " + next.toUpperCase() + "\nTime: " + getTime());
                    location.reload()
                }, 200);
                break;
            case 0:
                updateNext()
        }
    }
}

setInterval(() => {
    seconds++;
    time.innerText = getTime();
}, 1000);
