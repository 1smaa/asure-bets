import { urlBuilder, Cookie, getBiri } from "./packages.js";
import { loginBanner, tableReset } from "./banners.js";
class Bet {
    constructor(row) {
        this.row = row;
    }
    createHTML() {
        let string = "<tr>";
        for (let j = 0; j < this.row.length; j++) {
            if (j == 4) {
                continue;
            }
            if (this.row[j] == "None") {
                string += "<td></td>"
            }
            else if (typeof this.row[j] === 'string' && this.row[j].includes("https")) {
                string += `<td><img src="${this.row[j]}"></td>`;
            }
            else {
                string += `<td>${this.row[j]}</td>`;
            }
        }
        return string + "</tr>";
    }
}

class Login {
    static toggleLogin() {
        if (this.checkLogin()) {
            document.getElementById("body-wp").removeChild(document.getElementById("lg-banner-wp"));
            document.getElementById("table").style.display = "inline-flex";
        }
        else {
            document.getElementById("table").style.display = "none";
            let b = document.getElementById("body-wp");
            b.innerHTML = loginBanner + b.innerHTML;
        }
    };

    static checkLogin() {
        return document.getElementById("body-wp").getAttribute("lg-shown") == "true";
    };
}

function elaborateData(data) {
    document.getElementById("bet-table").innerHTML = tableReset;
    for (const key in data) {
        let bet = new Bet(data[key]);
        let html = bet.createHTML();
        document.getElementById("bet-table").innerHTML += html;
    }
    document.getElementById("table").style.display = "inline-flex";
}

async function loadData(BIRI) {
    const BASE = "http://127.0.0.1:5000";
    const ENDPOINT = "fetch";
    const SPORT = document.getElementById("sport").value;
    const BOOKMAKER = document.getElementById("bookmaker").value;
    const PARAMS = {
        biri: BIRI,
        sport: SPORT == "Tutti" ? "None" : SPORT,
        bookmaker: BOOKMAKER == "Tutti" ? "None" : BOOKMAKER
    }
    if (!(Cookie.checkCookie("session"))) {
        alert("Accedi al tuo account");
        return;
    }
    fetch(urlBuilder(BASE, ENDPOINT, PARAMS), {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + Cookie.getCookie("session")
        }
    })
        .then(response => response.json())
        .then((data) => {
            elaborateData(data);
            document.getElementById("update-btn").classList.remove("update-animation");
        })
        .catch((err) => alert("Qualcosa è andato storto, se il problema persiste, contattaci."))
}

const resetOptions = () => {
    let options = document.getElementsByTagName("option");
    for (let i = 0; i < options.length; i++) {
        options[i].style.backgroundColor = "white";
    }
}

const animate = () => {
    document.getElementById("update-btn").classList.add("update-animation");
}

const update = async (e) => {
    try {
        if (!e.target.matches("#update-btn")) {
            if (e.target.tagName === "OPTION") {
                let element = e.target;
                resetOptions();
                element.style.backgroundColor = "grey";
            }
            return;
        };
    }
    catch { }
    if (Login.checkLogin()) { Login.toggleLogin() };
    animate();
    const BIRI = getBiri();
    await loadData(BIRI);
}

document.addEventListener("click", update)

window.addEventListener("load", (e) => {
    const session = Cookie.getCookie("session");
    if (session == "") {
        Login.toggleLogin();
    } else {
        update(e);
    }
})