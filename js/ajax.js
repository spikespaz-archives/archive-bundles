function buildQuery(params) {
    let buffer = [];

    Object.keys(params).forEach(function(key) {
        buffer.push(key + "=" + encodeURIComponent(params[key]));
    });

    return "?" + buffer.join("&");
}


function ajaxPost(dest, params, payload, callback) {
    let request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                callback(request.responseText);
            }
        }
    };

    request.open("POST", dest + buildQuery(params));
    request.send(null);
}
