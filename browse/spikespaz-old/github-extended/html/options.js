const formEl = document.getElementById("credentials-form");
let resetTimer;

formEl.addEventListener("submit", event => {
    event.preventDefault();

    let submitEl = event.target.querySelector("input[type='submit']");
    let formData = new FormData(event.target);

    let fieldData = {
        username: formData.get("username") || undefined,
        password: formData.get("password") || undefined,
        token: formData.get("token") || undefined
    };

    if (fieldData.token)
        fieldData = { token: fieldData.token };

    new Promise((resolve, reject) => {
        let github = new Octokat({ ...fieldData });

        github.rateLimit.fetch().then(result => {
            if (result.resources.core.limit > 60)
                resolve(result);
            reject(result);
        }).catch(reject);
    }).then(() => {
        return browser.storage.local.clear();
    }).then(() => {
        return browser.storage.local.set(fieldData);
    }).then(() => {
        submitEl.classList.remove("failure");
        submitEl.classList.add("success");
        submitEl.value = "Success!";

        clearInterval(resetTimer);
        updateUI();
    }).catch(() => {
        submitEl.classList.remove("success");
        submitEl.classList.add("failure");
        submitEl.value = "Failure!";
    }).then(() => {
        setTimeout(() => {
            submitEl.classList.remove("success", "failure");
            submitEl.value = "Save";
        }, 2000);
    });
});

function updateUI() {
    browser.storage.local.get().then(result => {
        formEl.querySelector("input[name='username']").value = result.username || "";
        formEl.querySelector("input[name='password']").value = result.password || "";
        formEl.querySelector("input[name='token']").value = result.token || "";

        let github = new Octokat(result);
        let displayEl = document.querySelector("#ratelimit-display>tbody");

        function startResetTimer() {
            github.rateLimit.fetch().then(result => {
                displayEl.innerHTML = `
                    <tr>
                        <td>${result.resources.core.limit}</td>
                        <td>${result.resources.core.remaining}</td>
                        <td id="reset-timer"></td>
                    </tr>
                `;

                let timerEl = document.getElementById("reset-timer");
                let resetTime = new Date(result.resources.core.reset * 1000).getTime();

                function updateTimer() {
                    let delta = resetTime - Date.now();

                    if (delta < 0) {
                        clearInterval(resetTimer);
                        startResetTimer();

                        return;
                    }

                    let minutes = Math.floor((delta % 3600000) / 60000);
                    let seconds = Math.floor((delta % 60000) / 1000);

                    timerEl.innerText = `${minutes}m ${seconds}s`;
                }

                updateTimer();
                resetTimer = setInterval(updateTimer, 1000);
            });
        }

        startResetTimer();
    });
}

updateUI();
