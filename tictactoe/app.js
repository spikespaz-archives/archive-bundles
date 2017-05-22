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
    for (cell = 0; cell < 3; cell++) {
        console.log(cell * 3, cell * 3 + 1, cell * 3 + 2);
        if ((grid[cell * 3].innerText === grid[cell * 3 + 1].innerText && grid[cell * 3 + 1].innerText === grid[cell * 3 + 2].innerText && grid[cell * 3].innerText) ||
            (grid[cell].innerText === grid[cell + 3].innerText && grid[cell + 3].innerText === grid[cell + 6].innerText && grid[cell].innerText)) {
            return 1
        }
    }
    
    if ((grid[0].innerText === grid[4].innerText && grid[4].innerText === grid[8].innerText && grid[0].innerText) ||
        (grid[2].innerText === grid[4].innerText && grid[4].innerText === grid[6].innerText && grid[2].innerText)) {
        return 1
        
    } else {
        full = 0;

        for (cell in grid) {
            if (grid[cell].innerText) {
                full++
            }
        }

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
