//step 1: get DOM
let nextDom = document.getElementById('main-next');
let prevDom = document.getElementById('main-prev');

let carouselDom = document.querySelector('.main-carousel');
let SliderDom = carouselDom.querySelector('.main-carousel .main-list');
let thumbnailBorderDom = document.querySelector('.main-carousel .main-thumbnail');
let thumbnailItemsDom = thumbnailBorderDom.querySelectorAll('.main-item');
let timeDom = document.querySelector('.main-carousel .main-time');

thumbnailBorderDom.appendChild(thumbnailItemsDom[0]);
let timeRunning = 3000;
let timeAutoNext = 7000;

nextDom.onclick = function(){
    showSlider('main-next');    
}

prevDom.onclick = function(){
    showSlider('main-prev');    
}
let runTimeOut;
let runNextAuto = setTimeout(() => {
    nextDom.click(); 
}, timeAutoNext)
function showSlider(type){
    let  SliderItemsDom = SliderDom.querySelectorAll('.main-carousel .main-list .main-item');
    let thumbnailItemsDom = document.querySelectorAll('.main-carousel .main-thumbnail .main-item');
    
    if(type === 'main-next'){
        SliderDom.appendChild(SliderItemsDom[0]);
        thumbnailBorderDom.appendChild(thumbnailItemsDom[0]);
        carouselDom.classList.add('main-next');
    }else{
        SliderDom.prepend(SliderItemsDom[SliderItemsDom.length - 1]);
        thumbnailBorderDom.prepend(thumbnailItemsDom[thumbnailItemsDom.length - 1]);
        carouselDom.classList.add('main-prev');
    }
    clearTimeout(runTimeOut);
    runTimeOut = setTimeout(() => {
        carouselDom.classList.remove('main-next');
        carouselDom.classList.remove('main-prev');
    }, timeRunning);

    clearTimeout(runNextAuto);
    runNextAuto = setTimeout(() => {
        nextDom.click();
    }, timeAutoNext)
}  
