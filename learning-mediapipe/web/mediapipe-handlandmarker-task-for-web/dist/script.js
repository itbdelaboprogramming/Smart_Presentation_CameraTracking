import { HandLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0";
const demosSection = document.getElementById("demos");
let handLandmarker = undefined;
let runningMode = "IMAGE";
let enableWebcamButton;
let webcamRunning = false;

let isHandsClose = false; // Variabel untuk melacak apakah tangan berdekatan
let closeTimeout; // Variabel untuk menyimpan timeout

const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");

let lastVideoTime = -1;
let results = undefined;

const createHandLandmarker = async () => {
    const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm");
    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`,
            delegate: "GPU"
        },
        runningMode: runningMode,
        numHands: 2
    });
    demosSection.classList.remove("invisible");
};

createHandLandmarker();

/********************************************************************
// Demo 2: Continuously grab image from webcam stream and detect it.
********************************************************************/

// Check if webcam access is supported.
const hasGetUserMedia = () => { var _a; return !!((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia); };

// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
    enableWebcamButton = document.getElementById("webcamButton");
    enableWebcamButton.addEventListener("click", enableCam);
}
else {
    console.warn("getUserMedia() is not supported by your browser");
}

// Enable the live webcam view and start detection.
function enableCam(event) {
    if (!handLandmarker) {
        console.log("Wait! objectDetector not loaded yet.");
        return;
    }
    if (webcamRunning === true) {
        webcamRunning = false;
        enableWebcamButton.innerText = "ENABLE PREDICTIONS";
    }
    else {
        webcamRunning = true;
        enableWebcamButton.innerText = "DISABLE PREDICTIONS";
    }
    // getUsermedia parameters.
    const constraints = {
        video: true
    };
    // Activate the webcam stream.
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
    });
}

// Fungsi untuk mengecek jarak tangan
function checkHandDistance(firstHand, secondHand) {
    const thumbDistance = Math.abs(firstHand[4].x - secondHand[4].x);
    return thumbDistance < 0.15; // Sesuaikan ambang sesuai kebutuhan
}

// Fungsi yang akan diaktifkan ketika tangan berdekatan
function onHandsClose() {
    console.log("Tangan berdekatan, menjalankan fungsi...");
    // Di sini Anda dapat menjalankan fungsi atau kode lain yang Anda inginkan
}

// Fungsi yang akan diaktifkan ketika tangan berjauhan
function onHandsApart() {
    console.log("Tangan berjauhan, menjalankan fungsi...");
    // Di sini Anda dapat menjalankan fungsi atau kode lain yang Anda inginkan
}

// Fungsi untuk mengatur timeout jika tangan berubah
function setCloseTimeout() {
    closeTimeout = setTimeout(() => {
        onHandsClose(); // Jika timeout tercapai, tangan tetap berdekatan
        isHandsClose = true;
    }, 1000); // Waktu timeout dalam milidetik (1 detik dalam contoh ini)
}

// Fungsi untuk membatalkan timeout jika tangan berubah dalam waktu yang lebih cepat
function cancelCloseTimeout() {
    if (closeTimeout) {
        clearTimeout(closeTimeout);
        closeTimeout = null;
    }
}

async function predictWebcam() {
    canvasElement.style.width = video.videoWidth;
    canvasElement.style.height = video.videoHeight;
    canvasElement.width = video.videoWidth;
    canvasElement.height = video.videoHeight;

    // Now let's start detecting the stream.
    if (runningMode === "IMAGE") {
        runningMode = "VIDEO";
        await handLandmarker.setOptions({ runningMode: "VIDEO" });
    }

    let startTimeMs = performance.now();
    if (lastVideoTime !== video.currentTime) {
        lastVideoTime = video.currentTime;
        results = handLandmarker.detectForVideo(video, startTimeMs);
    }

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    if (results.landmarks.length != 0) {
        // Zoom 
        // detection 2 hands
        if (results.landmarks.length == 2) {
            const firstHand = results.landmarks[0];
            const secondHand = results.landmarks[1];

            // Mengecek jarak tangan
            const handsClose = checkHandDistance(firstHand, secondHand);

            if (handsClose && !isHandsClose) {
                // Tangan berdekatan dan sebelumnya tidak berdekatan
                onHandsClose(); // Jalankan fungsi saat tangan berdekatan
                isHandsClose = true;
                setCloseTimeout(); // Atur timeout untuk menunggu perubahan
            } else if (!handsClose && isHandsClose) {
                // Tangan berjauhan dan sebelumnya berdekatan
                cancelCloseTimeout(); // Batalkan timeout jika tangan berubah terlalu cepat
                onHandsApart(); // Jalankan fungsi saat tangan berjauhan
                isHandsClose = false;
            }
        }

        for (const landmarks of results.landmarks) {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {
                color: "#00FF00",
                lineWidth: 5
            });
            drawLandmarks(canvasCtx, landmarks, { color: "#FF0000", lineWidth: 2 });
        }
    }

    canvasCtx.restore();

    // Call this function again to keep predicting when the browser is ready.
    if (webcamRunning === true) {
        window.requestAnimationFrame(predictWebcam);
    }
}