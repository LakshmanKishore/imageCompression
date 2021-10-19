let imageInput = document.querySelector('.imageInput');
let image = document.querySelector('.image');
let imageSize = document.querySelector('.imageSize');
let ci = document.querySelector('.ci');
let ciSize = document.querySelector('.ciSize');
let originalImage = document.querySelector('.originalImage');
let compression = document.querySelector('.compression');
let compress = document.querySelector('.compress');
let spinner = document.querySelector('.spinner');

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function setImageSize(imagePath, htmlSizeDiv) {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", imagePath, true);
    xhr.responseType = "arraybuffer";
    xhr.onreadystatechange = function () {
        if (this.readyState == this.DONE) {
            htmlSizeDiv.innerHTML = formatBytes(this.response.byteLength);
        }
    };
    xhr.send(null);
}

function loadImage(src) {
    originalImage.hidden = false;
    image.src = src;
    compression.hidden = true
    setImageSize(image.src, imageSize)
}

function loadFile(e) {
    if (e.target.files) {
        let imageFile = e.target.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(imageFile);
        reader.onloadend = function (e) {
            loadImage(e.target.result);
            imageSize.innerHTML = formatBytes(imageFile.size);
        }
    }
}

function submit() {
    spinner.hidden = false;
}

setImageSize(ci.src, ciSize)

imageInput.addEventListener('change', loadFile);
compress.addEventListener('click', submit);