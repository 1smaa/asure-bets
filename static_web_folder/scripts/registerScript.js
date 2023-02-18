import { cyrb53, urlBuilder, Cookie, getBiri } from "./packages.js";

const BASE = "http://127.0.0.1:5000"

let fetchData = async () => {
    let name = document.getElementById("name").value;
    let last = document.getElementById("last").value;
    let email = document.getElementById("email").value;
    let pwd = document.getElementById("pwd").value;
    let aff = document.getElementById("aff").value;
    let biri = getBiri();
    return {
        name: name,
        lastName: last,
        email: email,
        password: cyrb53(pwd),
        biri: biri,
        affiliation: aff
    }
}

document.addEventListener("click", async (e) => {
    if (!e.target.matches("#register")) { return; }
    e.preventDefault();
    let json = await fetchData();
    fetch(urlBuilder(BASE, "rgstr"),
        {
            "headers": {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            "method": "POST",
            "body": JSON.stringify(json)
        })
        .then(response => response.json())
        .then((data) => {
            if (data === null) { throw 500 }
            alert(data.message);
            if (data.status == 1) {
                Cookie.storeCookie("session", data["session"]);
            }
            window.location.replace("home.html");
        })
        .catch((err) => { alert("There was an error while registering your account.") })
})