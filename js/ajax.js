export class Ajax {
    constructor(user=null, password=null) {
        this.user = user;
        this.password = password;

        this.requests = [];
    }

    GET(url, params={}, data=null, async=true, user=this.user, password=this.password) {
        let request = this.request("GET", params, data, async, user, password);
        request.responseJSON = () => { return JSON.parse(request.responseText); };

        this.requests.push(request);

        return request;
    }

    POST(url, params={}, data=null, async=true, user=this.user, password=this.password) {
        let request = this.request("POST", params, data, async, user, password);
        request.responseJSON = () => { return JSON.parse(request.responseText); };

        this.requests.push(request);

        return request;
    }

    PUT(url, params={}, data=null, async=true, user=this.user, password=this.password) {
        let request = this.request("PUT", params, data, async, user, password);
        request.responseJSON = () => { return JSON.parse(request.responseText); };

        this.requests.push(request);

        return request;
    }

    DELETE(url, params={}, data=null, async=true, user=this.user, password=this.password) {
        let request = this.request("DELETE", params, data, async, user, password);
        request.responseJSON = () => { return JSON.parse(request.responseText); };

        this.requests.push(request);

        return request;
    }

    static request(method, url, params={}, data=null, async=true, user=this.user, password=this.password) {
        let request = new XMLHttpRequest();

        request.onreadystatechange = function () {
            if (request.readyState === XMLHttpRequest.DONE) {
                return request;
            }
        };
        
        request.open("POST", url + this.buildQuery(params), async, user, password);
        request.send(data);
    }

    static buildQuery(params) {
        let buffer = [];

        Object.keys(params).forEach(function(key) {
            buffer.push(key + "=" + encodeURIComponent(params[key]));
        });

        return "?" + buffer.join("&");
    }
}
