// Get the canvas element form the page
const canvas = document.getElementById("viewer");
const ctx = canvas.getContext("2d");

canvas.width = screen.width;
canvas.height = screen.height;

function fullscreen() {
    if (canvas.webkitRequestFullScreen) {
        canvas.webkitRequestFullScreen();
        canvas.style.display = "block";
    } else if (canvas.mozRequestFullScreen) {
        canvas.mozRequestFullScreen();
        canvas.style.display = "block";
    } else if (canvas.msRequestFullScreen) {
        canvas.msRequestFullScreen();
        canvas.style.display = "block";
    } else {
        alert("Your browser does not support full screen canvas.")
    }
}

function floodScreen(color) {
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function pickBand(previous) {
    let choice = Math.random();
    let color = choice < 1/3 ? "red" : choice < 2/3 ? "green" : "blue";

    if (color === previous) {
        pickBand(previous)
    } else {
        previous = color;
        return color
    }
}

document.onclick = () => {
    let previous;

    fullscreen();

    setInterval(() => {
        floodScreen(pickBand(previous))
    }, 10);
};
