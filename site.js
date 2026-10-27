// The support email shown on the support and privacy pages (written by script so it isn't plain text for scrapers).
const EMAIL = "hello@viniciusramos.com";
document.querySelectorAll("a.email").forEach(a => { a.href = "mailto:" + EMAIL + "?subject=HexBeat"; a.textContent = EMAIL; });
