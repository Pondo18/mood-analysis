const parts = [];
let mediaRecorder;
let blob;
let public_stream;

async function record() {
    navigator.mediaDevices.getUserMedia({audio: false, video: true}).then(stream => {
        document.getElementById("video").srcObject = stream;
        mediaRecorder = new MediaRecorder(stream)
        mediaRecorder.start(1000)
        mediaRecorder.ondataavailable = function (e) {
            parts.push(e.data)
        }
        public_stream = stream
        document.getElementById("submit_video").disabled = false;
    });
}

function set_submit_file_enabled() {
    document.getElementById("submit_file").disabled = false;
}

let form = document.getElementById("stop_recording");
form.addEventListener("submit", function (event) {
    mediaRecorder.stop();
    public_stream.getTracks() // get all tracks from the MediaStream
        .forEach(track => track.stop()); // stop each of them
    blob = new Blob(parts, {
        type: "video/webm"
    });
    document.getElementById("video").srcObject = null;
    let form_data = new FormData();
    form_data.append("blob_video", blob, "blob_video");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', form.action, true);
    xhr.send(form_data);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            document.write(xhr.response);
        }
    }
    event.preventDefault();
});
