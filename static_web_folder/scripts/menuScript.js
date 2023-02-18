import { Cookie } from "./packages.js";
import {
    loginMenu, logoutMenu
} from "./banners.js";

window.addEventListener("load", (e) => {
    let menu = document.getElementById("menu");
    if (Cookie.getCookie("session") == "") {
        menu.innerHTML += loginMenu;
    } else {
        menu.innerHTML += logoutMenu;
    }
})