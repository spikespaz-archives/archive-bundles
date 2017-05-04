hide_intro = document.getElementById("hide-intro");

var intro_hidden = false;

hide_intro.onclick = function() {
    if (intro_hidden) {
        document.getElementById("intro").style.display = "block";
        hide_intro.textContent = "Ok, hide this please!";
        intro_hidden = false;
    } else {
        document.getElementById("intro").style.display = "none";
        hide_intro.textContent = "Show me the intro!";
        intro_hidden = true;
    }
};
