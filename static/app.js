let images = [];
let currentIndex = 0;

function openLightbox(index) {
    images = [...document.querySelectorAll(".detail-gallery img")]
                .map(img => img.getAttribute("src"));

    currentIndex = index;

    document.getElementById("lightbox-img").src = images[currentIndex];
    document.getElementById("lightbox").style.display = "flex";
}

function closeLightbox() {
    document.getElementById("lightbox").style.display = "none";
}

function changeImg(step) {
    currentIndex = (currentIndex + step + images.length) % images.length;
    document.getElementById("lightbox-img").src = images[currentIndex];
}