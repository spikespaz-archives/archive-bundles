export class Ajax {
    constructor(user, password) {
        this.user = user;
        this.password = password;

        this.requests = [];
    }

    GET(url, params={}, data=null, async=true) {
        let request = Ajax.request("GET", url, params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    POST(url, params={}, data=null, async=true) {
        let request = Ajax.request("POST", url, params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    PUT(url, params={}, data=null, async=true) {
        let request = Ajax.request("PUT", url, params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    DELETE(url, params={}, data=null, async=true) {
        let request = Ajax.request("DELETE", url, params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    static request(method, url, params={}, data=null, async=true, user=undefined, password=undefined) {
        let request = new XMLHttpRequest();

        request.onreadystatechange = function () {
            if (request.readyState === XMLHttpRequest.DONE) {
                return request;
            }
        };
        
        request.open(method, url + this.buildQuery(params), async, user, password);
        request.send(data);
    }

    static buildQuery(params, listPrefix="", listDelim=";", listSuffix="") {
        let buffer = [];

        Object.keys(params).forEach(function(key) {
            let value = params[key];

            if (value instanceof Array && typeof value.join === "function") {
                value = listPrefix + value.join(listDelim) + listSuffix;
            }

            buffer.push(key + "=" + encodeURIComponent(value));
        });

        return "?" + buffer.join("&");
    }
}
