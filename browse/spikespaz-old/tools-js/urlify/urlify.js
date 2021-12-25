(function(document) {
    var ENTER = 13;
    var KEY_V = 86;

    var CLOSURE = "https://closure-compiler.appspot.com/compile";

    var INPUT_TEXTAREA = document.getElementById("input-textarea");
    var OUTPUT_TEXTAREA = document.getElementById("output-textarea");

    var STATUS_MESSAGE = document.getElementById("status-message");
    var STATUS_CONTENT = document.getElementById("status-content");

    function showStatus(message) {
        STATUS_CONTENT.innerText = message;
        STATUS_MESSAGE.style.display = "block";
    }

    function resetStatus(delay) {
        setTimeout(function() {
            STATUS_CONTENT.innerText = "";
            STATUS_MESSAGE.style.display = "none";
        }, delay);
    }

    function closureCompiler(value, callback) {
        var request = new XMLHttpRequest();

        request.onreadystatechange = function () {
            if (request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 200) {
                    callback(request.responseText);
                }
            }
        };

        var fields = [,
            "compilation_level=ADVANCED_OPTIMIZATIONS",
            "output_format=text",
            "output_info=compiled_code",
            "language=ECMASCRIPT6",
            "language_out=ECMASCRIPT3",
            "js_code=" + encodeURIComponent(value)
        ];

        request.open("POST", CLOSURE + "?" + fields.join("&").substr(1));
        request.send(null);

        return value;
    }
    
    function htmlEntities(str) {
        return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    INPUT_TEXTAREA.onkeyup = function (event) {
        if (event.which === KEY_V && event.ctrlKey || event.which === ENTER && event.ctrlKey) {
            var script = INPUT_TEXTAREA.value;

            showStatus("Computing...");

            script = closureCompiler(script, function(result) {
                script = "javascript:" + result;
                script = htmlEntities(script);
                script = script.replace("\n", "");

                OUTPUT_TEXTAREA.value = script;

                resetStatus();

                OUTPUT_TEXTAREA.click();
            });
        }
    };

    OUTPUT_TEXTAREA.onclick = function() {
        OUTPUT_TEXTAREA.focus();
        OUTPUT_TEXTAREA.select();
    };
})(document);