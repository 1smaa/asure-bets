import { Cookie } from "./packages.js";

document.addEventListener("click", (e) => {
    if (e.target.matches("#logout")) {
        Cookie.eraseCookie("session");
        window.location.reload();
    }
})