function formatNum(num) {
    return num > 999 ? (num / 1000).toFixed(1) + "k" : num;
}

function createDownloadButton(btnUrl, numUrl, count) {
    let buttonEl = document.createElement("li");
    let labelEl = document.createElement("a");
    let iconEl = document.createElement("span");
    let countEl = document.createElement("a");

    labelEl.className = "btn btn-sm btn-with-count";
    labelEl.title = "Go to the highest release version";
    labelEl.href = btnUrl;
    labelEl.innerText = " Download";

    iconEl.innerHTML = "<svg width='16' height='16' class='octicon octicon-desktop-download v-align-text-bottom' viewBox='0 0 16 16' version='1.1' aria-hidden='true'><path fill-rule='evenodd' d='M4 6h3V0h2v6h3l-4 4-4-4zm11-4h-4v1h4v8H1V3h4V2H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h5.34c-.25.61-.86 1.39-2.34 2h8c-1.48-.61-2.09-1.39-2.34-2H15c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1z'></path></svg>";

    countEl.className = "social-count";
    countEl.href = numUrl;
    countEl.innerText = count;

    buttonEl.id = "downloads-social-button";

    labelEl.insertBefore(iconEl, labelEl.childNodes[0]);

    buttonEl.appendChild(labelEl);
    buttonEl.appendChild(countEl);

    return buttonEl;
}

function documentReady() {
    return new Promise((resolve) => {
        document.addEventListener("DOMContentLoaded", resolve);
    });
}

function beginPreload() {
    let urlMatch = window.location.pathname.match(/\/([\w-]+)\/([\w-]+)/);
    console.log(urlMatch);

    Promise.all([
        getSortedReleases(urlMatch[1], urlMatch[2]),
        documentReady()
    ]).then((values) => {
        let releaseJson = values[0];

        let actionsEl = document.getElementsByClassName("pagehead-actions")[0];
        let dlCount = 0;

        for (release of releaseJson)
            for (asset of release.assets)
                dlCount += asset.download_count;

        let buttonEl = createDownloadButton(
            releaseJson[0].html_url,
            window.location.pathname + "/releases",
            formatNum(dlCount)
        );

        actionsEl.appendChild(buttonEl);
    });
}

beginPreload();
