const video = document.getElementById('video')
const canvas = document.getElementById('canvas')
const snap = document.getElementById('snap')
const errorMsgElement = document.getElementById('spanErrorMsg')
const prediction = document.getElementById('prediction')
var image;

const constraints = {
    audio: false,
    video: {
        width:200, height: 200
    }
}

async function init(){
    try{
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream)
    }
    catch(e){
        errorMsgElement.innerHTML = `navigator.getUserMedia.error:${e.toString()}`
    }
}

function handleSuccess(stream){
    window.stream = stream;
    video.srcObject = stream;
}

init();

var context = canvas.getContext('2d');
context.translate(200, 0);
context.scale(-1, 1);
snap.addEventListener("click", function(){
    context.drawImage(video, 0, 0, 200, 200);
    var imgURI = canvas.toDataURL('image/jpeg');
    var entry = {
        image: imgURI,
    };
    fetch('/predict', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
            .then(response => response.json())
        .then(data => {
        console.log(data)
        $("#prediction").text(data.JSON);
    })
        .catch(error => {
        console.error(error)
    })
});

function create() {
    var bet_amount = document.getElementById('bet_amount').value;
    var event_name = document.getElementById('event_name').value;
    var entry = {
        bet_amount: bet_amount,
        event_name: event_name
    };
    console.log(entry)
    fetch('/create', {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry),
    })
    .then(response => location.reload(true));
}