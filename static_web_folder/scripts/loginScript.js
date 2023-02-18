import { Cookie, cyrb53, urlBuilder, getBiri } from "./packages.js";

const BASE = "http://127.0.0.1:5000"
const getParams = async () => {
    let email = document.getElementById("email").value;
    let pwd = document.getElementById("pwd").value;
    return {
        email: email,
        password: cyrb53(pwd),
        biri: getBiri()
    }
}

const elaborateData = async () => {
    const PARAMS = await getParams();
    fetch(urlBuilder(BASE, "auth"), {
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        "method": "POST",
        "body": JSON.stringify(PARAMS)
    })
        .then(response => response.json())
        .then((data) => {
            let sessionKey = data["session"];
            Cookie.storeCookie("session", sessionKey);
            alert("Accesso avvenuto correttamente.");
            window.location.replace("home.html");
        })
        .catch((err) => alert(err));
}

document.addEventListener("click", (e) => {
    if (!e.target.matches("#login")) { return; }
    elaborateData();
})