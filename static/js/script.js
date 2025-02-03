function show_error(message) {
    var error_message = document.getElementById('error-message');
    error_message.innerHTML = message;
    error_message.style.display = "block";
    error_message.style.animation = "none";
    void error_message.offsetWidth;
    error_message.style.animation = "disappear 2s 1s ease-out forwards";
}

async function start_playing() {
    var response = await fetch('/setup/check_artists');
    var responseJSON = await response.json()
    if (!responseJSON['artists_exist']) {
        show_error("No artists added to play");
    }
    else {
        window.location.href = "/play";
    }
}

async function add_artist() {
    var input = document.getElementById('search');
    var search = input.value;
    input.value = "";
    if (search) {
        var original = input.placeholder;
        input.disabled = true;
        input.placeholder = "Searching...";
        var response = await fetch('/setup/add_artist?search=' + search);
        var responseJSON = await response.json()
        document.getElementById('artists').innerHTML = responseJSON['html'];
        if (!responseJSON['artist_found']) {
            show_error("Artist '" + search + "' not found");
        }
        input.placeholder = original;
        input.disabled = false;
        input.focus();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search");

    if (input) {
        input.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                add_artist();
            }
        });
    }
});

async function remove_artist(name) {
    var response = await fetch('/setup/remove_artist?name=' + encodeURIComponent(name));
    var responseTxt = await response.text()
    document.getElementById('artists').innerHTML = responseTxt;
}

async function guess(letter) {
    var response = await fetch('/game/guess?letter=' + letter);
    var responseTxt = await response.text();

    const contentElement = document.getElementById('content');
    const scrollPos = { x: window.scrollX, y: window.scrollY };

    const newImg = new Image();
    newImg.src = responseTxt.match(/src="([^"]+)"/)[1];

    newImg.onload = () => {
        contentElement.innerHTML = responseTxt;
        window.scrollTo(scrollPos.x, scrollPos.y);
    };

    if (newImg.complete) {
        contentElement.innerHTML = responseTxt;
        window.scrollTo(scrollPos.x, scrollPos.y);
    }
}

async function new_game() {
    var response = await fetch('/game/start');
    var responseJSON = await response.json()

    const contentElement = document.getElementById('content');
    const scrollPos = { x: window.scrollX, y: window.scrollY };

    const newImg = new Image();
    newImg.src = responseJSON['html'].match(/src="([^"]+)"/)[1];

    newImg.onload = () => {
        contentElement.innerHTML = responseJSON['html'];
        window.scrollTo(scrollPos.x, scrollPos.y);
    };

    if (newImg.complete) {
        contentElement.innerHTML = responseJSON['html'];
        window.scrollTo(scrollPos.x, scrollPos.y);
    }

    if (responseJSON['win'])
        guess('A');
}