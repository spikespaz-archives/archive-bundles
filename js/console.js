function stringSplice(original, position, remove, replacement) {
    return original.slice(0, position) + replacement + original.slice(position + Math.abs(remove))
}


function registerConsole(console_element) {
    var console_buffer = console_element.getElementsByClassName("console-buffer")[0];
    // var console_lines = console_buffer.getElementsByClassName("console-line");
    var console_input = document.createElement("input");
    var console_display = nextDisplayLine(console_buffer);

    console_input.setAttribute("class", "console-input");
    console_input.setAttribute("type", "text");

    console_element.appendChild(console_input);

    function setDisplayLine(value) {
        console_display.innerHTML = value;
    }

    function getSelectionRange() {
        return [console_input.selectionStart, console_input.selectionEnd];
    }

    function getCursorElement() {
        return console_display.getElementsByClassName("console-cursor")[0];
    }

    function getInputNoWrap() {
        return console_input.value.replace(/ /g, "\xa0");
    }

    function getRenderedSelection() {
        var selection_range = getSelectionRange();
        var input_value = getInputNoWrap()

        if (selection_range[0] == selection_range[1])
            return stringSplice(input_value, selection_range[0], 0, "<span class='console-cursor'></span>");
        else
            return stringSplice(input_value, selection_range[0], selection_range[1] - selection_range[0],
                                "<mark>" + input_value.slice(selection_range[0], selection_range[1]) + "</mark>")
    }

    function nextDisplayLine() {
        var console_line = document.createElement("li");
        console_line.classList.add("console-line");

        var console_display = document.createElement("p");
        console_display.classList.add("console-display");

        console_line.appendChild(console_display);
        console_buffer.appendChild(console_line);

        return console_display
    }

    console_element.onclick = function() {
        setDisplayLine(getRenderedSelection());
        console_input.focus();
    };

    console_input.onblur = function() {
        setDisplayLine(getInputNoWrap());
    };

    console_element.onkeyup = function() {
        setDisplayLine(getRenderedSelection());
    };

    console_element.onkeydown = function() {
        setDisplayLine(getRenderedSelection());
    };

    console_element.onkeypress = function() {
        setDisplayLine(getRenderedSelection());
    };
}


window.onload = function() {
    registerConsole(document.getElementById("main-console"));
}
