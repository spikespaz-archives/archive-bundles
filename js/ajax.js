export class Ajax {
    constructor(user, password) {
        this.user = user;
        this.password = password;

        this.requests = [];
    }

    GET(url, params={}, data=null, async=true) {
        let request = this.request("GET", params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    POST(url, params={}, data=null, async=true) {
        let request = this.request("POST", params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    PUT(url, params={}, data=null, async=true) {
        let request = this.request("PUT", params, data, async, this.user, this.password);
        request.responseJSON = JSON.parse(request.responseText);

        this.requests.push(request);

        return request;
    }

    DELETE(url, params={}, data=null, async=true) {
        let request = this.request("DELETE", params, data, async, this.user, this.password);
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
        
        request.open("POST", url + this.buildQuery(params), async, user, password);
        request.send(data);
    }

    static buildQuery(params, listPrefix="", listDelim=";", listSuffix="") {
        let buffer = [];

        Object.keys(params).forEach(function(key) {
            let value = params[key];

            if (value instanceof Array && typeof value.join === "function") {
                value = listPrefix + value.join(listDelim) + listSuffix;
            } else if (value === "") {} else {
                buffer.push(key + "=" + encodeURIComponent(value));
            }
        });

        return "?" + buffer.join("&");
    }
}
