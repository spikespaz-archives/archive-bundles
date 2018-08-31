// Code adapted from my Search Deflector project's updating code.
// https://github.com/spikespaz/search-deflector/blob/master/source/updater.d

const RELEASES_URL = "https://api.github.com/repos/{{author}}/{{repository}}/releases";

function downloadLatestRelease(author, repository, filename) {
    getLatestRelease(author, repository).then((release) => {
        for (asset of release["assets"])
            if (asset["name"] == filename) {
                window.open(asset["browser_download_url"], "_self");
                return;
            }
    }).catch(window.alert);
}

function getLatestRelease(author, repository) {
    return new Promise((resolve, reject) => {
        getSortedReleases(author, repository).then((releases) => {
            resolve(releases[0]);
        }).catch(reject);
    });
}

function getSortedReleases(author, repository) {
    return new Promise((resolve, reject) => {
        const response = getJson(
            RELEASES_URL.replace("{{author}}", author).replace("{{repository}}", repository));

        response.then((apiJson) => {
            apiJson.sort((first, second) => !compareVersions(first["tag_name"], second["tag_name"]));

            resolve(apiJson);
        });

        response.catch(reject);
    });
}

// Get and parse JSON for the specified URL, and return a promise.
function getJson(url) {
    return new Promise((resolve, reject) => {
        let request = new XMLHttpRequest();

        request.open("GET", url, true);
        request.responseType = "json";

        request.onload = () => {
            if (request.status == 200)
                resolve(request.response);
            else
                reject(request.status, request.response);
        };

        request.send();
    });
}

function compareVersions(firstVer, secondVer) {
    let first = firstVer.split(".");
    let second = secondVer.split(".");

    while (first.length > second.length) {
        if (first[0] != 0)
            return true;

        first.shift();
    }

    while (second.length > first.length) {
        if (second[0] != 0)
            return false;

        second.shift();
    }

    for (parts of first.map((item, index) => [item, second[index]])) {
        if (parts[0] > parts[1])
            return true;
        else if (parts[1] > parts[0])
            return false;
    }

    return false;
}
