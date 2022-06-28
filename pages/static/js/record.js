const parts = [];
let mediaRecorder;

function start_recording() {
    console.log("Starting");
    navigator.mediaDevices.getUserMedia({audio: false, video: true}).then(stream => {
        document.getElementById("video").srcObject = stream;
        mediaRecorder = new MediaRecorder(stream)
        mediaRecorder.start(1000)
        mediaRecorder.ondataavailable = function (e) {
            parts.push(e.data)
        }
    });
}

function stop_recording() {
    console.log("Stopping");
    mediaRecorder.stop();
    const blob = new Blob(parts, {
        type: "video/webm"
    });
    const url = URL.createObjectURL(blob);
    document.getElementById("recorded_video").value = blob;
    document.getElementById("video").srcObject = null;
}

// window.onload = function () {
//
//
//     navigator.mediaDevices.getUserMedia({audio: false, video: true}).then(stream => {
//         document.getElementById("video").srcObject = stream
//         document.getElementById("start_record").onclick = function () {
//             mediaRecorder = new MediaRecorder(stream)
//             mediaRecorder.start(1000)
//             mediaRecorder.ondataavailable = function (e) {
//                 parts.push(e.data)
//             }
//         }
//     });
//
//     document.getElementById("stop_recording").onclick = function () {
//         mediaRecorder.stop();
//         const blob = new Blob(parts, {
//             type: "video/webm"
//         });
//         const url = URL.createObjectURL(blob);
//         document.getElementById("recorded_video").value = blob;
//     }
// }