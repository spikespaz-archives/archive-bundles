HIDE_INTRO = document.getElementById("hide-intro");
INTRO = document.getElementById("intro");
STORY_EDIT = document.getElementById("story-edit");

var intro_hidden = false;

HIDE_INTRO.onclick = function() {
    if (intro_hidden) {
        INTRO.style.display = "block";
        this.textContent = "Ok, hide this please!";
        intro_hidden = false;
    } else {
        INTRO.style.display = "none";
        this.textContent = "Show me the intro!";
        intro_hidden = true;
    }
};

STORY_EDIT.onkeyup = function(event) {
    if (event.which === 221) {
        this.innerHTML = this.innerText.replace(/\[([\w\s]+)]/g, "<code>[$1]</code>");
    }
};
