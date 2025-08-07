function showSpinner() {
    var submitBtn = document.getElementById('submit-btn');
    var submitText = document.getElementById('submit-text');
    var spinner = document.getElementById('spinner');
    submitBtn.disabled = true;
    submitText.classList.add('d-none');
    spinner.classList.remove('d-none');
}

document.addEventListener("DOMContentLoaded", function () {
    let loader = document.getElementById("loading-animation");
    window.onload = function () {
        loader.style.display = "none";
    };
});
