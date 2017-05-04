HIDE_INTRO = document.getElementById("hide-intro");
INTRO = document.getElementById("intro");
STORY = document.getElementById("story-edit");

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

STORY.onkeyup = function(event) {
    if (event.which === 221) {
        STORY.innerHTML = STORY.innerText.replace(/\[([\w\s]+)]/g, "<code>[$1]</code> ");
    }
};
