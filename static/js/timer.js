
const showTimer = (element, startTime) => {
    const seconds = 120;
    var delta = Date.now() - startTime;     // milliseconds
    var deltaSeconds = delta / (1000);
    if (deltaSeconds < seconds) {
        // display minutes remaining
        element.innerText = `Resend OTP in ${Math.round(seconds - deltaSeconds)} seconds`;
        element.disabled = true;
    } else {
        element.innerText = 'Resend OTP';
        element.disabled = false;
    }
    setTimeout(function (){showTimer(element,startTime)}, 1000);
}

window.onload = ()=>{
    const startTime = Date.now();
    const btn = document.getElementById("resend-btn");
    showTimer(btn,startTime)
}
