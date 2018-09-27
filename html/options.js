const formEl = document.getElementById("credentials-form");

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
            if (result.rate.limit > 60)
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
    }).catch((reason) => {
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

browser.storage.local.get().then(result => {
    formEl.querySelector("input[name='username']").value = result.username || "";
    formEl.querySelector("input[name='password']").value = result.password || "";
    formEl.querySelector("input[name='token']").value = result.token || "";
});
