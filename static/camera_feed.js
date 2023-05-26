camera1 = document.getElementById('66e52bf814774b7be4c5a8d4dbe7c80476f82c4d79110cf6d87a0d6a0b539803')
camera1.srcObject.getTracks()
.forEach(track => track.stop());

var myVideoInputs = [];
async function doGetDevicesInfo () {
    await navigator.mediaDevices.enumerateDevices()
        .then(results => {
            //console.log(results);
            results.forEach(result => {
                if (result.kind === "videoinput") {
                    console.log(result);
                    myVideoInputs.push(result);
                }
            })
        })
        .catch(error =>  {
            console.log(error);
        })
}

doGetDevicesInfo()

async function startCamera(myVideoInput, whichCamera) {
    if(myVideoInput === undefined) { 
        console.log(navigator.mediaDevices.enumerateDevices());
        console.log('myVideoInput is undefined') 
        return;
    }
    await navigator.mediaDevices.getUserMedia( {
        video: {
            width: 200,
            height: 100,
            devideId: myVideoInput.devideId
        }
    })
    .then(stream => {
        whichCamera.srcObject = stream
    })
    .catch(error => {
        console.log(error)
    })
}

function doStartCamera (button) {
    const id = button.id;
    switch (id) {
        case 'startCamera1':
            startCamera(myVideoInputs[0], camera1);
            break;
        case 'startCamera2':
            startCamera(myVideoInputs[1], camera2);
            break;
    }
}

