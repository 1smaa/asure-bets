import { getBiri, urlBuilder, Cookie } from "./packages.js";

const BASE = "http://127.0.0.1:5000"



class Reframe {
    static get() {
        return document.getElementById("news-wp");
    }
    static set() {
        Reframe.get().setAttribute("reframe", "true");
    }
    static check() {
        let element = Reframe.get();
        return (element.hasAttribute("reframe") && element.getAttribute("reframe") == "true");
    }
    static unset() {
        Reframe.get().setAttribute("reframe", "false");
    }
}

const deactivateScroll = () => {
    document.getElementById("news-wp").setAttribute("scroll", "none")
}

const elaborateNews = (data) => {
    if (data.length == 0) {
        deactivateScroll();
        return;
    }
    for (const row in data) {
        let source = data[row][2];
        fetch(urlBuilder(BASE, "gtsrc", {
            link: source
        }), {
            method: "GET",
            mode: "cors",
            cache: "no-cache"
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById("news-wp").innerHTML += data["html"];
            })
    }
}

const getNews = async () => {
    let wp = document.getElementById("news-wp");
    if (wp.getAttribute("scroll") != "activated") { return; }
    let page = parseInt(wp.getAttribute("page-n")) + 1;
    wp.setAttribute("page-n", page.toString());
    const BIRI = getBiri();
    if (!Cookie.checkCookie("session")) {
        alert("Accedi al tuo account.");
        return;
    }
    const SESSION = Cookie.getCookie("session");
    fetch(urlBuilder(BASE, "gtnws", {
        biri: BIRI,
        page: page
    }), {
        method: "GET",
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + SESSION
        }
    })
        .then(response => response.json())
        .then(data => {
            elaborateNews(data["result"]);
        })
        .catch((err) => alert(err));
}
//INSERT INTO news(page,date,link) VALUES (1,"05/01/2023","news/news1.html");
window.onload = getNews();
window.onscroll = function (ev) {
    if (Reframe.check()) { return; }
    Reframe.set();
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        getNews();
    }
    setTimeout(Reframe.unset, 2000);
};