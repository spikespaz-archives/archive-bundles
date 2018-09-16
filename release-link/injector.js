((document, script, callback) => {
    if (document.querySelector('script[src=\'' + script + '\']')) {
        callback();
        return;
    }

    let scriptEl = document.createElement('script');

    scriptEl.setAttribute('src', script);
    scriptEl.setAttribute('type', 'text/javascript');
    scriptEl.onload = () => callback();

    document.body.appendChild(scriptEl);
})(document, 'https://spikespaz.github.io/tool-scripts/release-link/releases.js', () =>
    downloadLatestRelease('spikespaz', 'search-deflector', 'SearchDeflector-Installer.exe')
);
