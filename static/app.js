let imageInput = document.querySelector('.imageInput');
let image = document.querySelector('.image');
let imageSize = document.querySelector('.imageSize');
let imageUpload = document.querySelector('.imageUpload');
let ci = document.querySelectorAll('.ci');
let ciSize = document.querySelectorAll('.ciSize');
let compress = document.querySelector('.compress');

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function setImageSize(imagePath, htmlSizeDiv) {
    var xhr = new XMLHttpRequest();
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
    imageUpload.hidden = false;
    image.src = src;
}

// function loadFile(e) {
//     if (e.target.files) {
//         let imageFile = e.target.files[0];
//         let reader = new FileReader();
//         reader.readAsDataURL(imageFile);
//         reader.onloadend = function (e) {
//             loadImage(e.target.result);
//             imageSize.innerHTML = formatBytes(imageFile.size);
//         }
//     }
// }

function showCompressedImage(){
    for (let index = 1; index <= ciSize.length; index++) {
        const element = ciSize[index-1];
        setImageSize(`/static/ci${index}.jpeg`, element);
    }
}

// function startCompress(){
//     console.log("Started Compressing");
//     fetch("/compress")
// }

showCompressedImage();
setImageSize("/static/original.jpg",imageSize)

// imageInput.addEventListener('change', loadFile);
// compress.addEventListener('click',startCompress);