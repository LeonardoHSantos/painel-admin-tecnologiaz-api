console.log("script_links.js carregados...")

let link_actual = window.location;
let nameClassAux = null;
if (link_actual.pathname == "/") {
    nameClassAux = "home"
}
else if (link_actual.pathname.includes("config-admin")) {
    nameClassAux = "config-admin";
}
else if (link_actual.pathname.includes("autenticacao-iqoption")) {
    nameClassAux = "autenticacao-iqoption"
}
// ----------------------------------------------------------------------------------------------
let content_footer = document.querySelector(".content-footer");
if (link_actual.pathname.includes("config-admin") | link_actual.pathname.includes("/")) {
    content_footer.style.position = "relative";
} else {
    content_footer.style.position = "fixed";
    content_footer.style.bottom = "0";
    content_footer.style.width = "100%";
}
// ----------------------------------------------------------------------------------------------
try {
    let classEditnavbar = document.querySelector(`.link-navbar-${nameClassAux}`);
    classEditnavbar.style.color = "var(--color-white-1)";
    classEditnavbar.style.color = "var(--color-base-1)";
} catch (error) {}



