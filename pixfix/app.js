const flood = document.getElementById("flood");
const fullscreen = document.getElementById("fullscreen");
const noSleep = new NoSleep();

fullscreen.onclick = () => {
    let isFullscreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
        (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
        (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
        (document.msFullscreenElement && document.msFullscreenElement !== null);

    if (!isFullscreen) {
        if (document.body.requestFullscreen) {
            document.body.requestFullscreen();
        } else if (document.body.mozRequestFullScreen) {
            document.body.mozRequestFullScreen();
        } else if (document.body.webkitRequestFullScreen) {
            document.body.webkitRequestFullScreen();
        } else if (document.body.msRequestFullscreen) {
            document.body.msRequestFullscreen();
        }

        noSleep.enable()
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }

        noSleep.disable()
    }
};

let counter = 0;

setInterval(
    () => {
        if (counter === 0) {
            flood.style.background = "red"
        } else if (counter === 1) {
            flood.style.background = "green"
        } else if (counter === 2) {
            flood.style.background = "blue"
        }

        if (counter < 3) {
            counter++;
        } else {
            counter = 0;
        }
    }, 10
);

let dragging = false;
let floodX, floodY, initialX, initialY;

document.onmousedown = (event) => {
    dragging = true;
    initialX = event.clientX;
    initialY = event.clientY;
    floodX = parseInt(flood.offsetLeft);
    floodY = parseInt(flood.offsetTop);
};

document.onmouseup = () => {
    dragging = false;
};

document.onmousemove = (event) => {
    if (dragging) {
        let deltaX = (initialX - event.clientX) * -1;
        let deltaY = (initialY - event.clientY) * -1;

        flood.style.left = (floodX + deltaX) + "px";
        flood.style.top = (floodY + deltaY) + "px";

    }
};
