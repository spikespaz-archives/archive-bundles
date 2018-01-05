function getInputLine(buffer_list) {
    var input_lines = buffer_list.getElementsByClassName("console-input-line");
    return input_lines[input_lines.length - 1];
}


function getSelectionRange(input_element) {
    return [input_element.selectionStart, input_element.selectionEnd];
}


function getFormattedSelection(input_text, selection_range) {
    if (selection_range[0] == selection_range[1])
        return input_text.substring(0, selection_range[0]) +
               "&#9608;" +
               input_text.substring(selection_range[0] + 1, input_text.length);
    else
        return input_text.substring(0, selection_range[0]) +
               "<mark>" +
               input_text.substring(selection_range[0], selection_range[1]) +
               "</mark>" +
               input_text.substring(selection_range[1], input_text.length);
}


function registerConsole(console_app) {
    var input_box = console_app.getElementsByClassName("console-input-box")[0];
    var buffer_list = console_app.getElementsByClassName("console-buffer-list")[0];

    var console_blink = true;
    var selection_range;

    getInputLine(buffer_list).innerHTML = input_box.value;

    console_app.onclick = function() input_box.focus();

    function updateInputLine() {
        getInputLine(buffer_list).innerHTML =
            getFormattedSelection(input_box.value, getSelectionRange(input_box));
    }

    function keyUpdate() {
        updateInputLine();
        console_blink = true;
        console_app.scrollTop = console_app.scrollHeight;
    };

    input_box.onkeyup = keyUpdate;
    input_box.onkeydown = keyUpdate;
    input_box.onkeypress = keyUpdate;

    window.setInterval(function() {
        if (document.activeElement == input_box) {
            selection_range = getSelectionRange(input_box);

            if (selection_range[1] > selection_range[0] ||
                 console_blink && selection_range[0] == selection_range[1])
                updateInputLine();
            else
                getInputLine(buffer_list).innerHTML = input_box.value;

            console_blink = !console_blink;
        } else
            getInputLine(buffer_list).innerHTML = input_box.value;
    }, 700);
}


window.onload = function() {
    registerConsole(document.getElementsByClassName("console-application-wrapper")[0]);
}
