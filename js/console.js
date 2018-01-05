var console_input_text = document.getElementById("console-input-text");
var console_input_display = document.getElementById("console-input-display");

var console_input_blink = true;


function getSelection() {
    return [console_input_text.selectionStart, console_input_text.selectionEnd];
}


function getSelectionText(selection) {
    if (selection[0] == selection[1]) {
        return console_input_text.value.substring(0, selection[0]) + "&#9608;" +
               console_input_text.value.substring(selection[0] + 1, console_input_text.value.length);
    } else {
        return console_input_text.value.substring(0, selection[0]) +
               "<mark>" + console_input_text.value.substring(selection[0], selection[1]) + "</mark>" +
               console_input_text.value.substring(selection[1], console_input_text.value.length);
    }
}


function updateDisplay() {
    console_input_display.innerHTML = getSelectionText(getSelection());
}


window.onload = function() {
    console_input_text.focus();
    console_input_text.onblur = console_input_text.focus;

    console_input_text.onkeyup = updateDisplay;
    console_input_text.onkeydown = updateDisplay;
    console_input_text.onkeypress = updateDisplay;


    window.setInterval(function() {
        var selection = getSelection();


        if (selection[1] > selection[0]) {
            console_input_display.innerHTML = getSelectionText(selection);
        } else if (console_input_blink && selection[0] == selection[1]) {
            console_input_display.innerHTML= getSelectionText(selection);
        } else {
            console_input_display.innerHTML = console_input_text.value;
        }

        console_input_blink = !console_input_blink;
    }, 700);
}
