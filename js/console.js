function nextInputLine(buffer) {
    var buffer_line = document.createElement("li");
    buffer_line.className = "console-buffer-line";

    var input_line = document.createElement("p");
    input_line.className = "console-input-line";
    input_line.innerHTML = "<span class='cursor blink'></span>"

    buffer_line.appendChild(input_line);
    buffer.appendChild(buffer_line);

    return input_line
}


function registerConsole(console_element) {
    var input_box = document.createElement("input");
    input_box.setAttribute("class", "console-input-box");
    input_box.setAttribute("type", "text");
    console_element.appendChild(input_box);

    console_element.onclick = function() {input_box.focus()};
    console_element.onblur = function() {};

    var buffer = console_element.getElementsByClassName("console-buffer-list")[0];

    var current_line = nextInputLine(buffer);
}


window.onload = function() {
    registerConsole(document.getElementById("main-console"));
}
