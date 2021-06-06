var video = document.querySelector("#videoElement");

const fps = 3;
var socket = io("https://192.168.29.223:5001")

socket.on('connect', function() {
    setInterval(() => {
      socket.send(getFrame())
    }, 1000/fps);
    });

socket.on('message',function(msg){
    document.querySelector("#status").innerHTML = msg;
})


const getFrame = () => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const data = canvas.toDataURL('image/png');
  return data;
}


if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}


