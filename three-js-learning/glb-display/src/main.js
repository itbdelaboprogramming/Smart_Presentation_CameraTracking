import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/Addons.js';
import { 
    HandLandmarker,
    GestureRecognizer,
    FilesetResolver,
    DrawingUtils
} from '@mediapipe/tasks-vision';

const canvas = document.querySelector('canvas')
const scene =  new THREE.Scene()

const loader = new GLTFLoader()
let obj; 
loader.load('/glb/MSD700_ダンプタイプ.glb', (gltf) => {
    obj = gltf.scene
    scene.add(obj)
}, (xhr) => {
    console.log((xhr.loaded / xhr.total * 100) + '% loaded')
}, (error) => {
    console.log(error)
});

const light = new THREE.DirectionalLight(0xffffff, 1)
light.position.set(2, 2, 5)
scene.add(light)


const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)   
camera.position.set(0, 1, 2);
scene.add(camera)   

const renderer = new THREE.WebGLRenderer({
    canvas: canvas
})




renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.shadowMap.enabled = true   

function animate() {
    requestAnimationFrame(animate)
    renderer.render(scene, camera)
}

animate()

document.addEventListener('keydown', function(event) {
    switch(event.key) {
        case 'ArrowUp':
            // Code to execute when the up arrow is pressed
            camera.position.z += 0.1
            break;
        case 'ArrowDown':
            camera.position.z -= 0.1
            break;
        case 'ArrowLeft':
            obj.position.x -= 0.1
            break;
        case 'ArrowRight':
            obj.position.x += 0.1
            break;
        case ',':
            obj.rotation.y += 0.1
            break;
        case '.':
            obj.rotation.y -= 0.1
            break;
    }
});


/* MediaPipe Section */

const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");
const gestureOutput = document.getElementById("gesture_output");

function hasGetUserMedia() {
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

let runningMode = "VIDEO";
let gestureRecognizer;
const createGestureRecognizer = async () => {
    const vision = await FilesetResolver.forVisionTasks(
      "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm"
    );
    gestureRecognizer = await GestureRecognizer.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath:
          "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
        delegate: "GPU"
      },
      runningMode: runningMode
    });
    };
await createGestureRecognizer();



if (hasGetUserMedia()) {
    enableCam();
} else {
  console.warn("getUserMedia() is not supported by your browser");
}
const videoHeight = "360px";
const videoWidth = "480px";

// Enable the live webcam view and start detection.
function enableCam(event) {
  if (!gestureRecognizer) {
    alert("Please wait for gestureRecognizer to load");
    return;
  }
  const constraints = {
    video: true
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
    video.srcObject = stream;
    video.addEventListener("loadeddata", predictWebcam);
  });
}
const webcamRunning = true;

let lastVideoTime = -1;
let results = undefined;
async function predictWebcam() {
  const webcamElement = document.getElementById("webcam");
  if (runningMode === "IMAGE") {
    runningMode = "VIDEO";
    await gestureRecognizer.setOptions({ runningMode: "VIDEO" });
  }
  let nowInMs = Date.now();
  if (video.currentTime !== lastVideoTime) {
    lastVideoTime = video.currentTime;
    results = gestureRecognizer.recognizeForVideo(video, nowInMs);
  }

  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  const drawingUtils = new DrawingUtils(canvasCtx);

  canvasElement.style.height = videoHeight;
  webcamElement.style.height = videoHeight;
  canvasElement.style.width = videoWidth;
  webcamElement.style.width = videoWidth;

  if (results.landmarks) {
    console.log(1)
    console.log(results.landmarks)
    for (const landmarks of results.landmarks) {
      drawingUtils.drawConnectors(
        landmarks,
        GestureRecognizer.HAND_CONNECTIONS,
        {
          color: "#00FF00",
          lineWidth: 5
        }
      );
      drawingUtils.drawLandmarks(landmarks, {
        color: "#FF0000",
        lineWidth: 2
      });
    }
  }
  canvasCtx.restore();
  if (results.gestures.length > 0) {
    gestureOutput.style.display = "block";
    gestureOutput.style.width = videoWidth;
    const categoryName = results.gestures[0][0].categoryName;
    const categoryScore = parseFloat(
      results.gestures[0][0].score * 100
    ).toFixed(2);
    const handedness = results.handednesses[0][0].displayName;
    gestureOutput.innerText = `GestureRecognizer: ${categoryName}\n Confidence: ${categoryScore} %\n Handedness: ${handedness}`;
  } else {
    gestureOutput.style.display = "none";
  }
  if (webcamRunning === true) {
    window.requestAnimationFrame(predictWebcam);
  }
}
