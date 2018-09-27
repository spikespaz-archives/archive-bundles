let github;

function addDlButton() {
    let urlMatch = window.location.pathname.match(/\/([\w-]+)\/([\w-]+)/);
    let dlCount = 0;

    github.repos(urlMatch[1], urlMatch[2]).releases.fetchAll().then(response => {
        for (release of response)
            for (asset of release.assets)
                dlCount += asset.downloadCount;

        return response;
        // return response.reduce((a, b) => { !compareVersions(a.tag_name, b.tag_name) });
    }).then(response => {
        let buttonEl = createDlButton(
            response[0].htmlUrl,
            window.location.pathname + "/releases",
            dlCount.toLocaleString()
        );

        document.getElementsByClassName("pagehead-actions")[0].appendChild(buttonEl);
    });
}

function createDlButton(btnUrl, numUrl, count) {
    let buttonEl = document.createElement("li");

    buttonEl.id = "downloads-social-button";
    buttonEl.innerHTML = `
    <a class="btn btn-sm btn-with-count" href="${btnUrl}" title="Go to the latest release version">
    <svg width='16' height='16' class='octicon octicon-desktop-download v-align-text-bottom' viewBox='0 0 16 16' version='1.1' aria-hidden='true'>
    <path fill-rule='evenodd' d='M4 6h3V0h2v6h3l-4 4-4-4zm11-4h-4v1h4v8H1V3h4V2H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h5.34c-.25.61-.86 1.39-2.34 2h8c-1.48-.61-2.09-1.39-2.34-2H15c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1z'></path>
    </svg>
    Download
    </a>
    <a class="social-count" href="${numUrl}">${count}</a>
    `;

    return buttonEl;
}

browser.storage.local.get().then(result => {
    github = new Octokat(result);

    addDlButton();
});
