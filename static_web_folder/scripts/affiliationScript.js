import { Cookie, urlBuilder, getBiri } from "./packages.js";
import { loginBanner } from "./banners.js";

const displayLogin = () => {
    document.getElementById("body-wp").innerHTML = loginBanner;
}

const fetchData = (session, biri) => {
    const BASE = "http://127.0.0.1:5000";
    const ENDPOINT = "getaff";
    const PARAMS = {
        biri: biri
    }
    fetch(urlBuilder(BASE, ENDPOINT, PARAMS), {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + session
        }
    })
        .then((response) => {
            if (response.status == 401) {
                displayLogin();
            }
            return response.json()
        })
        .then((data) => {
            document.getElementById("code").innerHTML = data.response.aff;
            document.getElementById("first-level").innerHTML = data.response.firstLv;
            document.getElementById("second-level").innerHTML = data.response.secondLv;
        })
        .catch((e) => {
            displayLogin();
        })
}

window.addEventListener("load", async (e) => {
    let session = Cookie.getCookie("session");
    if (session == "") {
        displayLogin();
        return;
    }
    const BIRI = getBiri();
    fetchData(session, BIRI);
})