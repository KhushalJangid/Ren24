var destroy = document.querySelectorAll(".profile");
var i;
var w = window.innerWidth;
VanillaTilt.init(destroy);

function myFunction(i) {
    if (w <= 800) {
        destroy[i].vanillaTilt.destroy();
    }
}
for (i = 0; i < destroy.length; i++) {
    destroy[i].addEventListener('mousemove', unTilt);
}