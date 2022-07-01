const parts = [];
let mediaRecorder;
let blob;

async function record() {
    navigator.mediaDevices.getUserMedia({audio: false, video: true}).then(stream => {
        document.getElementById("video").srcObject = stream;
        mediaRecorder = new MediaRecorder(stream)
        mediaRecorder.start(1000)
        mediaRecorder.ondataavailable = function (e) {
            parts.push(e.data)
        }
    });
    const delay = ms => new Promise(res => setTimeout(res, ms));
    await delay(3000);
    mediaRecorder.stop();
    blob = new Blob(parts, {
        type: "video/webm"
    });
    document.getElementById("video").srcObject = null;
}

let form = document.getElementById("stop_recording");
form.addEventListener("submit", function (event) {
    let form_data = new FormData();
    form_data.append("blob_video", blob, "blob_video");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', form.action, true);
    xhr.send(form_data);
    event.preventDefault();
});
