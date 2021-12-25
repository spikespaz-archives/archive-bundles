let github;
let pageSize;

function addDlButton() {
    let urlMatch = window.location.pathname.match(/\/([\w-]+)\/([\w-]+)/);

    github.repos(urlMatch[1], urlMatch[2]).releases.fetch({ per_page: pageSize }).then(page => {
        let buttonEl = document.createElement("li");
        buttonEl.innerHTML = `
            <a class="btn btn-sm btn-with-count" href="${page.items[0].htmlUrl}" title="Go to the latest release version">
                <svg width='16' height='16' class='octicon octicon-desktop-download v-align-text-bottom' viewBox='0 0 16 16' version='1.1' aria-hidden='true'>
                    <path fill-rule='evenodd' d='M4 6h3V0h2v6h3l-4 4-4-4zm11-4h-4v1h4v8H1V3h4V2H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h5.34c-.25.61-.86 1.39-2.34 2h8c-1.48-.61-2.09-1.39-2.34-2H15c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1z'></path>
                </svg>
                Download
            </a>
            <a class="social-count" href="${window.location.pathname}/releases">0</a>
        `;

        document.querySelector(".pagehead-actions").appendChild(buttonEl);

        let countEl = buttonEl.querySelector(".social-count");
        let dlCount = 0;

        function addPageDlCount(page) {
            for (release of page.items)
                for (asset of release.assets) {
                    dlCount += asset.downloadCount;
                    countEl.innerText = dlCount.toLocaleString();
                }

            if (page.nextPage)
                page.nextPage.fetch().then(addPageDlCount);
        }

        addPageDlCount(page);
    });
}

browser.storage.local.get().then(result => {
    github = new Octokat({
        username: result.username,
        password: result.password,
        token: result.token
    });

    pageSize = result.pageSize || 30;

    addDlButton();
});
