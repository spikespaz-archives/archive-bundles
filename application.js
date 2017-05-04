HIDE_INTRO = document.getElementById("hide-INTRO");
INTRO = document.getElementById("INTRO");

var intro_hidden = false;

HIDE_INTRO.onclick = function() {
    if (intro_hidden) {
        INTRO.style.display = "block";
        HIDE_INTRO.textContent = "Ok, hide this please!";
        intro_hidden = false;
    } else {
        INTRO.style.display = "none";
        HIDE_INTRO.textContent = "Show me the intro!";
        intro_hidden = true;
    }
};
