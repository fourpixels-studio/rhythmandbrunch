function goBack() {
    window.history.back();
}
function copyToClipboard() {
    var copyText = document.getElementById("shareLink");
    var copyBtn = document.getElementById("copy-btn");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    copyBtn.innerHTML = "Link Copied";
}
function aos_init() {
    AOS.init({
        duration: 800,
        easing: 'slide',
        once: true,
        mirror: false
    });
}
window.addEventListener('load', () => {
    aos_init();
});