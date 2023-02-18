export const cyrb53 = (str, seed = 0) => {
    let h1 = 0xdeadbeef ^ seed,
        h2 = 0x41c6ce57 ^ seed;
    for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }

    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);

    return 4294967296 * (2097151 & h2) + (h1 >>> 0);
};

export const urlBuilder = (base, endpoint, params = null) => {
    let pString = params === null ? "" : "?";
    let pArr = [];
    for (const key in params) {
        pArr.push(`${key}=${encodeURIComponent(params[key])}`)
    }
    pString += pArr.join("&");
    return base + "/" + endpoint + pString;

}
export class Cookie {
    static storeCookie(cname, value) {
        let now = new Date();
        let time = now.getTime();
        let expireTime = time + (1000 * 3600 * 100);
        now.setTime(expireTime)
        document.cookie = `${cname}=${value}; expires=${now.toUTCString()};path=/;`;
    }
    static getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    static checkCookie(cname) {
        return document.cookie.includes(cname);
    }
    static eraseCookie(cname) {
        document.cookie = cname + '=; Max-Age=-99999999;';
    }
}

const getBiri = () => {
    return 460845891436985;
}