function shuffleArray(array) {
    // https://stackoverflow.com/a/12646864/8971202
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function copyToClipboard(text) {
    // https://stackoverflow.com/a/33928558/8971202
    if (window.clipboardData && window.clipboardData.setData) {
        // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
        return clipboardData.setData("Text", text);

    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        let textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}

function showTooltip(gifUrl, copied) {

    let message = copied ? ('Copied to clipboard: ' + gifUrl) : 'Something went wrong during copying to clipboard, check console.';
    Snackbar.show({text: message, pos: 'top-center', duration: 6942});
    if (!copied) {
        console.error('Error copying to clipboard: ' + copied);
    }
}

let gifs;
let app;

fetch('resources/cimrman.json')
    .then(response => response.json())
    .then(json => gifs = shuffleArray(json))
    .then(_ => console.log('Loaded ' + gifs.length + ' gifs.'))
    .then(_ => app = new Vue({
        el: '#app',
        data: {
            gifs: gifs,
            query: ''
        },
        methods: {
            copy: function (gif) {
                console.log('Copying ' + gif.url + ' to clipboard.')
                let copied = copyToClipboard(gif.url);
                showTooltip(gif.url, copied);
            },
            matches_query: function (keywords) {
                return this.query.split(/[ ]+/).every(
                    q => keywords.some(
                        k => RegExp(
                            q.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
                        ).test(k)));
            }
        },
        directives: {
            focus: {
                inserted: function (el) {
                    el.focus()
                }
            }
        }
    }));
